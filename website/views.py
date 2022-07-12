from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import requests
from bs4 import BeautifulSoup
import termtables as tt

views = Blueprint('views', __name__)

login_data = {
    '__RequestVerificationToken': '',
    'SCKTY00328510CustomEnabled': True,
    'SCKTY00436568CustomEnabled': True,
    'Database': 10,
    'VerificationOption': 'UsernamePassword',
    'LogOnDetails.UserName': '',
    'tempUN': '',
    'tempPW': '',
    'LogOnDetails.Password': ''
}

@views.route('/')
def home():
    if 'username' in request.cookies and 'password' in request.cookies:
        data = login_data
        data['LogOnDetails.UserName'] = request.cookies.get('username')
        data['LogOnDetails.Password'] = request.cookies.get('password')
        content = getName(data)
        return render_template("home1.html", content = content)
    return redirect(url_for('auth.login'))

@views.route('/classes')
def classes():
    if 'username' in request.cookies and 'password' in request.cookies:
        data = login_data
        data['LogOnDetails.UserName'] = request.cookies.get('username')
        data['LogOnDetails.Password'] = request.cookies.get('password')
        content = getClasses(data)
        return render_template("home.html", content = content)
    return redirect(url_for('auth.login'))

@views.route('/reportCard')
def reportCard():
    if 'username' in request.cookies and 'password' in request.cookies:
        data = login_data
        data['LogOnDetails.UserName'] = request.cookies.get('username')
        data['LogOnDetails.Password'] = request.cookies.get('password')
        content = getGrades(data)
        return render_template("reportCard.html", content = content)
    return redirect(url_for('auth.login'))

@views.route('/ipr')
def ipr():
    if 'username' in request.cookies and 'password' in request.cookies:
        data = login_data
        data['LogOnDetails.UserName'] = request.cookies.get('username')
        data['LogOnDetails.Password'] = request.cookies.get('password')
        content = getProgressReport(data)
        return render_template("progressReport.html", content = content)
    return redirect(url_for('auth.login'))

@views.route('/transcript')
def transcript():
    if 'username' in request.cookies and 'password' in request.cookies:
        data = login_data
        data['LogOnDetails.UserName'] = request.cookies.get('username')
        data['LogOnDetails.Password'] = request.cookies.get('password')
        content = getTranscript(data)
        return render_template("transcript.html", content = content)
    return redirect(url_for('auth.login'))

def getClasses(login_data):
    with requests.Session() as session:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        classes = []
        averages = []

        reportcardheader = ['Course', 'Description', 'Period', 'Teacher', '1st', '2nd', '3rd', 'Exam1', 'Sem1', '4th', '5th', '6th', 'Exam2', 'Sem2']
        reportcard = []

        finaldata = {}
        string = ''

        assignments = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/Assignments.aspx')
        content = BeautifulSoup(assignments.text, 'html.parser')

        for x in content.find_all('div', class_='AssignmentClass'):
            header = x.find('div', class_="sg-header")
            q = header.find('a', class_='sg-header-heading').text.strip()[12:]
            w = header.find('span', class_='sg-header-heading')
            classes.append(q.strip())
            averages.append(w.text.strip()[18:])

        string += ('\n\nClass Averages:\n')
        for i in range(len(classes)):
            string += ("\n" + classes[i] + " - " + averages[i])

        finaldata['classes'] = classes
        finaldata['averages'] = averages

        assignmentstable = []
        assignmentsrow = []

        finaldata['assignment'] = []
        finaldata['categories'] = []

        for x in content.find_all('table'):
            for row in x.find_all('tr'):
                for element in row.find_all('td'):
                    text = element.text.strip()
                    text = text.replace("*", "")
                    assignmentsrow.append(text.strip())
                assignmentstable.append(assignmentsrow)
                assignmentsrow = []
            if 'CourseCategories' in x.attrs['id']:
                finaldata['categories'].append(assignmentstable)
            elif 'CourseAssignments' in x.attrs['id']:
                finaldata['assignment'].append(assignmentstable)
            assignmentstable = []
        return finaldata

def getGrades(login_data):
    with requests.Session() as session:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        finaldata = {}
        reportcard = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/ReportCards.aspx')
        reportcardcontent = BeautifulSoup(reportcard.text, 'html.parser')
        headers = ['Course', 'Description', 'Period', 'Teacher', 'Room', '1st', '2nd', '3rd', 'Exam1', 'Sem1', '4th', '5th', '6th', 'Exam2', 'Sem2', 'CND1', 'CND2', 'CND3', 'CND4', 'CND5', 'CND6']
        row = []
        data = []
        finaldata['headers'] = headers
        counter = 0
        for x in reportcardcontent.find_all('td'):
            counter += 1
            # if counter <= 32:
            #     headers.append(x.text.strip())
            if counter > 32:
                row.append(x.text.strip())
            if (len(row) % 32 == 0) and (counter > 32):
                data.append(row)
                row = []
        for j in data:
            del j[31]
            del j[30]
            del j[29]
            del j[28]
            del j[27]
            del j[26]
            del j[25]
            del j[24]
            del j[23]
            del j[6]
            del j[5]
        finaldata['data'] = data
        return finaldata

def getProgressReport(login_data):
    with requests.Session() as session:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        finaldata = {}
        string = ''
        reportcard = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/InterimProgress.aspx')
        reportcardcontent = BeautifulSoup(reportcard.text, 'html.parser')
        with open('index3.html', 'w') as f:
            f.write(str(reportcardcontent))
        headers = []
        row = []
        data = []
        counter = 0
        for x in reportcardcontent.find_all('tr'):
            for c in x.find_all('td'):
                row.append(c.text.strip())
            data.append(row)
            row = []
        headers = data[0]
        data.pop(0)
        finaldata['headers'] = headers
        finaldata['data'] = data
        return finaldata

def getName(login_data):
    with requests.Session() as session:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        page = session.get('https://homeaccess.katyisd.org/HomeAccess/Home/WeekView')
        content = BeautifulSoup(page.text, 'html.parser')
        container = content.find('div', class_='sg-banner-menu-container')
        name = container.find('span')
        return name.text.strip()

def getTranscript(login_data):
    with requests.Session() as session:
        login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
        r = session.get(login_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
        post = session.post(login_url, data=login_data)
        finaldata = []
        year = []
        semester = []
        transcript = session.get('https://homeaccess.katyisd.org/HomeAccess/Content/Student/Transcript.aspx')
        content = BeautifulSoup(transcript.text, 'html.parser')
        with open('transcript.html', 'w') as f:
            f.write(str(content))
        maintable = content.find('table')
        maintable['class'] = "table-responsive border-dark"
        for x in content.find_all('table', class_='sg-asp-table'):
            x['class'] = "table table-bordered table-sm h-auto w-auto"

        for x in content.find_all('td', class_='sg-transcript-group'):
            x['class'] = "pr-3 pl-3 border-decondary"
        for x in content.find_all('table', attrs={'style':'width:100%'}):
            x['class'] = "table table-sm table-bordered"
        maintable.find('table', id='plnMain_rpTranscriptGroup_tblCumGPAInfo')['class'] = "table table-bordered table-sm h-auto w-auto mt-2"
        # for yearTable in maintable.find_all('tr'):
        #     for semTable in yearTable.find_all('td'):
        #         print(semTable.text)
        #         return
        return maintable
