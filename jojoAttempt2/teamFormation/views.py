from django.shortcuts import render
from django.shortcuts import redirect
from .models import csvUpload
from .forms import fileForm, colForm
import csv
from django.http import HttpResponse

# Create your views here.

#Step 1: Upload CSV File
def uploadFile(request):
    if request.method == 'POST':
        #clean up csv file
        data=[]
        form = request.FILES['csvFile']
        decoded_file = form.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            data.append(row) 
        #save data to session
        request.session['data'] = data
        return redirect('/columns/')
   
    else:
        form = fileForm()
    return render(request, 'home.html', {'form': form})

def pickColumns(request):
    if request.method == 'POST':
        # request.session['data'] = "Success!"
        data = request.session['data']
        return render(request, 'columns.html', {'data': data})
    else:
        form = colForm()
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

# views to manage session data 
def save_session_data(request):
    # manipulate data
    request.session['data'] = request.GET.get('data') #Does nothing
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
