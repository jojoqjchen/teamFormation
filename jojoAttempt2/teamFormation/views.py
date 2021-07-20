from django.shortcuts import render
from django.shortcuts import redirect
from .models import csvUpload, numberOfDownloads
from .forms import fileForm, colForm, teamSizeForm
import csv
from django.http import HttpResponse
import random
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import openpyxl
import os
import xlwt
from teamFormationCode.script import team_formation_tool
from django.contrib.auth.models import User
from django.db.models import Sum


# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile

# Create your views here.

def home(request):
    downloads = numberOfDownloads.objects.all().aggregate(Sum('download'))
    users = User.objects.all().count()
    print(downloads['download__sum'],users)
    return render(request, 'index.html', {'downloads':downloads['download__sum'],'users':users})

# Step 1: Upload CSV File
@login_required
def uploadFile(request):

    instructions = 'Enter your CSV or Excel file containing the information about the individuals.'

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

            return render(request, 'team-formation/team-formation-tool.html', {'form': fileForm(), 'step': '1', 'warning': 'Incorrect extension. Please make sure to upload a CSV or an Excel file.', 'instructions': instructions})

    # If the form is not filled -> we create it
    else:
        form = fileForm()

    return render(request, 'team-formation/team-formation-tool.html', {'form': form, 'step': '1', 'instructions': instructions})

# Step 2: Pick similar and different columns
@login_required
def pickColumns(request):

    instructions = 'Select the characteristics you want to optimize your teams on, or discard as many as you want.'
    colNames = list(request.session['colNames']) # list() may be unnecessary

    for idx, col in enumerate(colNames):
        colNames[idx] = str(colNames[idx]+' ('+str(idx+1)+')')

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

    return render(request, 'team-formation/team-formation-tool.html', {'form': form, 'step': '2', 'long': True, 'previous':"upload-teams", 'instructions': instructions})

 # Step 3: Enter team size
@login_required
def teamSize(request):

    instructions = 'Enter the ideal size for the teams.'

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

    return render(request, 'team-formation/team-formation-tool.html', {'form': form, 'step': '3', 'long': True, 'previous': "columns", 'instructions': instructions})

# IDEA: Gather the two "download" views -> i.e. passing the format of the output in the argument
@login_required
def downloadResultCsv(request):

    response = HttpResponse(
        content_type='text/csv',
        headers = {'Content-Disposition': 'attachment; filename="team-formation-results.csv"'},
    )

    colNames = list(request.session['colNames'])
    data = request.session['data']
    size = request.session['size']
    answers = request.session['answers']

    indexes = [i for i in range(len(colNames)) if int(answers[i])<3]

    report = team_formation_tool(data,colNames,indexes,int(size),False)

    colNames.append('Team')
    writer = csv.writer(response)
    writer.writerow(colNames) # To update

    for i in range(1,report.shape[0]):
        writer.writerow(list(report.iloc[i,:]))

    user = numberOfDownloads.objects.get(user = request.user)
    user.download+=1
    user.save()

    return response

@login_required
def downloadResultXlsx(request):
    response = HttpResponse(
        content_type = 'application/ms-excel',
        headers = {'Content-Disposition': 'attachment; filename="team-formation-results.xls"'}
    )

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Teams')

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    colNames = list(request.session['colNames'])
    data = request.session['data']
    size = request.session['size']

    answers = request.session['answers']

    indexes = [i for i in range(len(colNames)) if int(answers[i])<3]

    report = team_formation_tool(data,colNames,indexes,int(size),False)

    colNames.append('Team')
    nCol = len(colNames)

    for col_num in range(nCol):
        ws.write(0, col_num, colNames[col_num],font_style)

    font_style = xlwt.XFStyle()

    for i in range(1,report.shape[0]):
        for col_num in range(nCol):
            ws.write(i, col_num, str(report.iloc[i,col_num]), font_style)

    wb.save(response)

    user = numberOfDownloads.objects.get(user = request.user)
    user.download+=1
    user.save()

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
