from flask import Flask


def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hdsfgssdfgdfg'

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    app.run(debug=True)

if __name__ == '__main__':
    main()
