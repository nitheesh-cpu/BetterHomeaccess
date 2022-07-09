from flask import Blueprint, render_template, redirect, url_for, session, flash
import requests
from bs4 import BeautifulSoup
import numpy as np
import termtables as tt

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if 'username' in session:
        ses = session['username']
        return render_template("home1.html")
    return redirect(url_for('auth.login'))

@views.route('/classes')
def classes():
    if 'username' in session and 'login_data' in session:
        ses = session['username']
        content = getClasses(session['login_data'])
        return render_template("home.html", content = content)
    return redirect(url_for('auth.login'))

@views.route('/reportCard')
def reportCard():
    if 'username' in session and 'login_data' in session:
        ses = session['username']
        content = getGrades(session['login_data'])
        return render_template("reportCard.html", content = content)
    return redirect(url_for('auth.login'))

@views.route('/ipr')
def ipr():
    if 'username' in session and 'login_data' in session:
        ses = session['username']
        content = getProgressReport(session['login_data'])
        return render_template("progressReport.html", content = content)
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
        data = np.delete(data, [5, 6, 23, 24, 25, 26, 27, 28, 29, 30, 31], axis=1)
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
