from django.shortcuts import render
from django.shortcuts import redirect
from .models import csvUpload
from .forms import fileForm, colForm, teamSizeForm
import csv
from django.http import HttpResponse
import random
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import openpyxl
import os
import xlwt

# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile

# Create your views here.

def home(request):
    return render(request, 'index.html')

# Step 1: Upload CSV File
@login_required
def uploadFile(request):

    # If the form is filled
    if request.method == 'POST':
        # Validation may go here:
        # https://stackoverflow.com/questions/54403638/django-csv-file-validation-in-model-form-clean-method
        form = fileForm(request.POST, request.FILES) # Creating the form -> this allow to check for the correct extension
        if form.is_valid(): # Will mainly check if the file is CSV -> should enhance it to test size
            extension = os.path.splitext(str(request.FILES['csvFile']))[1]
            file = request.FILES['csvFile']
            data=[]

            ### TO MODIFY - I WANT TO TEST THE EXTENSION BUT NOT WORKING SO USED TRY
            if extension == '.xlsx':
                wb = openpyxl.load_workbook(file)
                # getting a particular sheet by name out of many sheets
                sheets = wb.sheetnames
                worksheet = wb[sheets[0]]

                # iterating over the rows and
                # getting value from each cell in row
                for row in worksheet.iter_rows():
                    row_data = list()
                    for cell in row:
                        row_data.append(str(cell.value))
                    data.append(row_data)

            elif extension == '.csv':
                # Getting the data from the form
                decoded_file = file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)
                for row in reader:
                    data.append(row)

            # Saving form data within the current session
            colNames = data.pop(0)
            #print("names" + str(colNames))  # For verification only
            request.session['colNames'] = colNames # Save column names in session
            request.session['data'] = data # Save the rest of the data in session
            #request.session['file'] = file
            # Go to the next step of the form
            return redirect('/columns/') # Redirect to the next step -> will call pickColumns

        else: # Currently, return home template with a WARNING - Incorrect extension

            return render(request, 'team-formation/team-formation-tool.html', {'form': fileForm(), 'step': '0%', 'warning': 'Incorrect extension. Please make sure to upload a csv file.'})

    # If the form is not filled -> we create it
    else:
        form = fileForm()

    return render(request, 'team-formation/team-formation-tool.html', {'form': form, 'step': '0%'})

# Step 2: Pick similar and different columns
def pickColumns(request):

    colNames = list(request.session['colNames']) # list() may be unnecessary

    # If the form is filled…
    if request.method == 'POST':
        # DOC: https://docs.djangoproject.com/en/3.2/ref/request-response/
        query = request.POST.copy() # !IMPORTANT
        query.pop('csrfmiddlewaretoken')
        answers = list(query.values()) # Get the answers provided for each of the columns in the initial form
        request.session['answers'] = answers
        return redirect('/teamsize/')

    # Else, we need to create a dynamic form with the columns from the imported csv file
    else:

        form = colForm(colNames) # See forms.py for further details

    return render(request, 'team-formation/team-formation-tool.html', {'form': form, 'step': '33%', 'long': True, 'previous':"upload-teams"})

 # Step 3: Enter team size
def teamSize(request):

    # If the form is filled
    if request.method == 'POST':

        # Playing with session data
        data = request.session['data']
        colNames = request.session['colNames']
        size = request.POST.get('size')
        answers = request.session['answers']
        col_answer = zip(colNames, answers)
        request.session['size'] = size

        # Outputting a CSV file
        ## Doc: https://docs.djangoproject.com/en/3.2/howto/outputting-csv/

        return render(request, 'team-formation/success.html', {
            'data': data,
            'size': size,
            'colNamesAnswers': col_answer,
        })

    # If the form has not been filled yet
    else:

        form = teamSizeForm()

    return render(request, 'team-formation/team-formation-tool.html', {'form': form, 'step': '67%', 'long': True, 'previous': "columns"})

def downloadResultCsv(request):

    response = HttpResponse(
        content_type='text/csv',
        headers = {'Content-Disposition': 'attachment; filename="team-formation-results.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['email', 'team number']) # To update
    data = request.session['data']
    size = request.session['size']
    for row in data:
        writer.writerow([str(row[3]),str(size)])
    print(writer)

    return response

def downloadResultXlsx(request):
    response = HttpResponse(
        content_type = 'application/ms-excel',
        headers = {'Content-Disposition': 'attachment; filename="team-formation-results.xls"'}
    )
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Teams')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['email', 'team number'] # To update

    data = request.session['data']
    size = request.session['size']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    for row in data:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

# def downloadResultPdf(request): https://www.youtube.com/watch?v=_zkYICsIbXI&ab_channel=CryceTruly
#     response = HttpResponse(
#         content_type = 'application/pdf',
#         headers = {
#         'Content-Disposition': 'attachment; filename="team-formation-results.pdf"',
#         'Content-Transfer-Encoding': 'binary',
#         }
#     )
#
#     data = request.session['data']
#
#     hmtl_string = render_to_string('team-formation/pdf-output.html',{'data': data})
#     html = HTML(string=html_string)
#
#     result = html.write_pdf()
#
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name,'rb')
#         response .write(output.read())
#
#     return response

### FURTHER TESTS

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
