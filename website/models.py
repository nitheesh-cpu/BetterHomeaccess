class User():
    def __init__(self, login_data, session):
        self.login_data = login_data
        self.session = session

    def getSession(self):
        return self.session

    def getLoginData(self):
        return self.login_data

    def logout(self):
        self.login_data = []
        self.session = None
