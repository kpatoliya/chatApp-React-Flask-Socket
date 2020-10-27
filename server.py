"""server.py"""
import os
import re
import flask
from flask import render_template, request
from flask_socketio import SocketIO
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from bot import Bot
import models

load_dotenv()

app = flask.Flask(__name__)
database_url = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.app = app
socketio = SocketIO(app, cors_allowed_origins='*')
totalUsers = {}
sockets = {}


def addToDb(name, message, email, profilePic):
    """function to add to database"""
    db_message = models.Messages(name, message, email, profilePic)
    db.session.add(db_message)
    db.session.commit()


@socketio.on('message')
def handle_message(msg):
    """function to handle message"""

    message = msg['message'].strip()
    profilePic = 'https://raw.githubusercontent.com/kpatoliya/kmps-petclinic/master/chatbot.jpg'
    regex = re.compile(r'^(?:http|ftp)s?://'  # http:// or https://
                       r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'
                       r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                       r'localhost|'  # localhost...
                       r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                       r'(?::\d+)?'  # optional port
                       r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if message.split(" ")[0] == '!!':
        addToDb(msg['name'], msg['message'], msg['email'], msg['profilePic'])
        socketio.emit('message_sent', {'message': msg})
        name = 'Bot'
        messageSet = ''
        msgArray = re.split(r"\s", message, 2)

        if msgArray[1] == 'weather':
            try:
                messageSet = Bot(msgArray[2]).getWeather()
            except IndexError:
                messageSet = Bot('Please enter city name!!').getWeather()
            socketio.emit('message_sent', {'message': {
                'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        elif msgArray[1] == 'gif':
            try:
                messageSet = Bot(msgArray[2]).getGif()
            except IndexError:
                messageSet = Bot('Please enter valid query!!').getGif()
            socketio.emit('message_sent', {'message': {
                'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        elif msgArray[1] == 'help':
            messageSet = Bot.botHelp()
            socketio.emit('message_sent', {'message': {
                'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        elif msgArray[1] == 'about':
            messageSet = Bot.botAbout()
            socketio.emit('message_sent', {'message': {
                'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        elif msgArray[1] == 'funtranslate':
            try:
                messageSet = Bot(msgArray[2]).funTranslate()
            except IndexError:
                messageSet = Bot('Please enter text to translate!!').funTranslate()
            socketio.emit('message_sent', {'message': {
                'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        elif msgArray[1] == 'randomjoke':
            messageSet = Bot.genRandomJoke()
            socketio.emit('message_sent', {'message': {
                'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        else:
            messageSet = Bot.botCommandInvalid()
            socketio.emit('message_sent', {'message': {
                'name': 'Bot', 'message': messageSet, 'profilePic': profilePic}})
        addToDb(name, messageSet, '', profilePic)

    elif re.match(regex, message):
        link = ''
        if message[-4:] == '.jpg' or message[-4:] == '.png' or message[-4:] == '.gif':
            link = Bot(message).renderImage()
            socketio.emit('message_sent', {'message': {
                'name': 'Bot', 'message': link, 'profilePic': profilePic}})
            addToDb('Bot', link, '', profilePic)
        else:
            link = Bot(message).renderLink()
            socketio.emit('message_sent', {'message': {
                'name': msg['name'], 'message': link, 'profilePic': msg['profilePic']}})
            addToDb(msg['name'], link, msg['email'], msg['profilePic'])

    else:
        socketio.emit('message_sent', {'message': msg})
        addToDb(msg['name'], msg['message'], msg['email'], msg['profilePic'])


@socketio.on('update_total_users')
def update_users(email):
    """function to handle on connection"""
    messagesArray = []
    socketId = request.sid
    all_messages = db.session.query(models.Messages).all()
    for message in all_messages:
        messagesArray.append({"name": message.user_name,
                              "message": message.text, "profilePic": message.profilePic})
    socketio.emit('on_connect', {'messages': messagesArray}, room=socketId)

    sockets[socketId] = email
    if email in totalUsers:
        totalUsers[email] += 1
    else:
        totalUsers[email] = 1
    socketio.emit('update_users', {'totalUsers': len(totalUsers)})


@socketio.on('disconnect')
def on_disconnect():
    """function to handle disconnection"""
    socketId = request.sid
    removeEmail = sockets.get(socketId)
    del sockets[socketId]
    if totalUsers.get(removeEmail) > 1:
        totalUsers[removeEmail] -= 1
    else:
        del totalUsers[removeEmail]
    socketio.emit('on_disconnect', {'totalUsers': len(totalUsers)})


@app.route('/')
def hello():
    """function to render main page"""
    return render_template('index.html')


if __name__ == '__main__':
    models.db.create_all()
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', 4000)
    )
