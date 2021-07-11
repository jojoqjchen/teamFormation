from django.shortcuts import render
from django.shortcuts import redirect
from .models import csvUpload
from .forms import fileForm, colForm, teamSizeForm
import csv
from django.http import HttpResponse

# Create your views here.

# Step 1: Upload CSV File
def uploadFile(request):

    if request.method == 'POST':
        # Validation may go here:
        # https://stackoverflow.com/questions/54403638/django-csv-file-validation-in-model-form-clean-method
        form = fileForm(request.POST, request.FILES) # Creating the form -> this allow to check for the correct extension
        if form.is_valid():
            data=[]
            form = request.FILES['csvFile'] # Recreating the form - hopefully not harmful
            decoded_file = form.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            for row in reader:
                data.append(row)
            # save column names separately
            colNames = data.pop(0)
            print("names" + str(colNames))
            request.session['colNames'] = colNames
            # save data to session
            request.session['data'] = data
            return redirect('/columns/')
        else:
            return render(request, 'home.html', {'form': fileForm(), 'warning': 'Incorrect extension. Please make sure to upload a csv file.'})
    else:
        form = fileForm()
    return render(request, 'home.html', {'form': form})

# Step 2: Pick similar and different columns
def pickColumns(request):
    if request.method == 'POST':
        # TODO: save columns
        return redirect('/teamsize/')
    else:
        colNames = list(request.session['colNames'])
        form = colForm(colNames)
    return render(request, 'home.html', {'form': form})

 # Step 3: Enter team size
def teamSize(request):
    if request.method == 'POST':
        data = request.session['data']
        colNames = request.session['colNames']
        size = request.POST.get('size')
        return render(request, 'success.html', {
            'data': data,
            'size': size,
            'colNames': colNames,
        })
    else:
        form = teamSizeForm()
    return render(request, 'home.html', {'form': form})

# test_session and test_delete Checks whether the browser accepted the cookie or not
def test_session(request):
    request.session.set_test_cookie()
    return HttpResponse("Testing session cookie")

def test_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("Cookie test passed")
    else:
        response = HttpResponse("Cookie test failed")
    return response

# EXAMPLE views to manage session data
def save_session_data(request):
    request.session['data'] = request.GET.get('data')
    return HttpResponse("Session Data Saved")

def access_session_data(request):
    response = []
    if request.session.get('data'):
        response.append(request.session.get('data'))
    if not response:
        return HttpResponse("No Session Data")
    else:
        return HttpResponse(response)

def delete_session_data(request):
    try:
        del request.session['data']
    except KeyError:
        pass
    return HttpResponse("Session Data Cleared")
