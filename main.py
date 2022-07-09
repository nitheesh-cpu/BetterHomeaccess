from website import create_app
from flask_socketio import SocketIO, emit
from flask import session, app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
