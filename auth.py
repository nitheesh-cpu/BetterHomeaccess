from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import requests
from bs4 import BeautifulSoup

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

    headers = {
        'Accept-Language' : 'en-US,en;q=0.5',
        'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 Safari/537.36'
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
