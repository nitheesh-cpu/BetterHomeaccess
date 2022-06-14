from website import create_app
from flask_socketio import SocketIO, emit

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

@SocketIO.on('disconnect')
def disconnect_user():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('login_data', None)
