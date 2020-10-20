import os
import re
import flask
from flask import render_template, request
from flask_socketio import SocketIO
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from bot import Bot

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API')
GIPHY_API_KEY = os.getenv('GIPHY_API')
database_url = os.getenv('DATABASE_URL')

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)
db.app = app
socketio = SocketIO(app, cors_allowed_origins='*')
totalUsers = {}
sockets = {}


@socketio.on('message')
def handle_message(msg):
    global totalUsers

    message = msg['message'].strip()
    profilePic = 'https://raw.githubusercontent.com/kpatoliya/kmps-petclinic/master/chatbot.jpg'
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if message.split(" ")[0] == '!!':
        db_message = models.Messages(msg['name'], msg['message'], msg['email'], msg['profilePic'])
        db.session.add(db_message)
        db.session.commit()

        name = 'Bot'
        messageSet = ''
        msgArray = re.split("\s", message, 2)

        if msgArray[1] == 'weather':
            try:
                messageSet = Bot(msgArray[2]).getWeather()
            except IndexError as error:
                messageSet = Bot('Please enter city name!!').getWeather()
            socketio.emit('message_sent', {'message': {'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        elif msgArray[1] == 'gif':
            try:
                messageSet = Bot(msgArray[2]).getGif()
            except IndexError as error:
                messageSet = Bot('Please enter valid query!!').getGif()
            socketio.emit('message_sent', {'message': {'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        elif msgArray[1] == 'help':
            messageSet = 'Working Prefixes: <br>!! about<br>!! weather --City Name' \
                         '<br>!! gif --Query <br> !! funtranslate --String to translate<br>!! randomjoke'
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        elif msgArray[1] == 'about':
            messageSet = "Hello! I'm Bot.<br>To learn more about my abilities type: !! help"
            socketio.emit('message_sent', {'message': {'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        elif msgArray[1] == 'funtranslate':
            try:
                messageSet = Bot(msgArray[2]).funTranslate()
            except IndexError as error:
                messageSet = Bot('Please enter text to translate!!').funTranslate()
            socketio.emit('message_sent', {'message': {'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        elif msgArray[1] == 'randomjoke':
            messageSet = Bot.genRandomJoke()
            socketio.emit('message_sent', {'message': {'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        else:
            messageSet = "Command Not Recognized!!"
            socketio.emit('message_sent', {'message': {'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})

        db_message = models.Messages(name, messageSet, '', profilePic)
        db.session.add(db_message)
        db.session.commit()
    elif re.match(regex, message):
        link = ''
        if message[-4:] == '.jpg' or message[-4:] == '.png' or message[-4:] == '.gif':
            link = Bot(message).renderLink()
            socketio.emit('message_sent', {'message': {'name': 'Bot', 'message': link, 'profilePic': profilePic}})
            db_message = models.Messages('Bot', link, '', profilePic)
            db.session.add(db_message)
            db.session.commit()
        else:
            link = "<u> <a href='" + message + "'>" + message + "</a></u>"
            socketio.emit('message_sent', {'message': {'name': msg['name'], 'message': link, 'profilePic': msg['profilePic']}})
            db_message = models.Messages(msg['name'], link, msg['email'], msg['profilePic'])
            db.session.add(db_message)
            db.session.commit()
    else:
        socketio.emit('message_sent', {'message': msg, 'totalUsers': len(totalUsers)})
        db_message = models.Messages(msg['name'], msg['message'], msg['email'], msg['profilePic'])
        db.session.add(db_message)
        db.session.commit()


@socketio.on('update_total_users')
def update_users(email):
    global totalUsers, sockets
    messagesArray = []
    socketId = request.sid
    all_messages = db.session.query(models.Messages).all()
    for message in all_messages:
        messagesArray.append({"name": message.user_name, "message": message.text, "profilePic": message.profilePic})
    socketio.emit('on_connect', {'messages': messagesArray, 'sid': socketId}, room=socketId)

    sockets[socketId] = email
    if email in totalUsers:
        totalUsers[email] += 1
    else:
        totalUsers[email] = 1

    print('Someone connected!')
    socketio.emit('update_users', {'totalUsers': len(totalUsers)})


@socketio.on('disconnect')
def on_disconnect():
    global sockets
    socketId = request.sid
    removeEmail = sockets.get(socketId)
    del sockets[socketId]
    global totalUsers
    if totalUsers.get(removeEmail) > 1:
        totalUsers[removeEmail] -= 1
    else:
        del totalUsers[removeEmail]

    print('Someone disconnected!')
    socketio.emit('on_disconnect', {'totalUsers': len(totalUsers)})


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    import models

    models.db.create_all()
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', 4000)
    )
