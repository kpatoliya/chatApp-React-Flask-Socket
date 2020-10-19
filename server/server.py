import json
import os
import re
import flask
import requests
from flask import render_template, request
from flask_socketio import SocketIO
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

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


class Bot:
    def __init__(self, string):
        self.string = string

    def getWeather(self):
        if self.string == 'Please enter city name!!':
            return self.string
        content = json.loads(requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + self.string +
                                          '&units=imperial&appid=' + WEATHER_API_KEY).text)
        if content['cod'] != 200:
            return 'Invalid Input!!'
        temperature = content['main']['temp']
        icon = content['weather'][0]['icon']
        condition = content['weather'][0]['description']
        return "<h4>" + self.string + ": " + str(temperature) + "°F" \
                                                                "<img src='http://openweathermap.org/img/w/" + icon + ".png'>" + condition + "</h4>"

    def getGif(self):
        if self.string == 'Please enter valid query!!':
            return self.string
        content = json.loads(requests.get('https://api.giphy.com/v1/gifs/search?api_key=' + GIPHY_API_KEY +
                                          '&q=' + self.string + '&limit=1&offset=0&rating=r&lang=en').text)
        if content['pagination']['total_count'] < 1:
            return 'Invalid Input!!'
        giphy = content['data'][0]['images']['downsized']['url']
        return "<h4> <img src='" + giphy + "' width='250' height='250'> </h4>"

    def funTranslate(self):
        if self.string == 'Please enter text to translate!!':
            return self.string
        content = json.loads(requests.get('https://api.funtranslations.com/translate/emoji.json?text='
                                          + self.string).text)
        retString = content['contents']['translated']
        return retString

    def renderLink(self):
        if self.string[-4:] == '.jpg' or self.string[-4:] == '.png' or self.string[-4:] == '.gif':
            return "<h4> <img src='" + self.string + "' width='250' height='250'> </h4>"
        else:
            return "<a href='" + self.string + "'> Click the Link </a>"

    @staticmethod
    def genRandomJoke():
        content = json.loads(requests.get('https://sv443.net/jokeapi/v2/joke/Programming?type=single').text)
        return content['joke']


@socketio.on('message')
def handle_message(msg):
    global totalUsers
    socketId = request.sid
    db_message = models.Messages(msg['name'], msg['message'], msg['email'], msg['profilePic'])
    db.session.add(db_message)
    db.session.commit()
    socketio.emit('message_sent', {'message': msg, 'totalUsers': len(totalUsers)})
    message = msg['message'].strip()
    profilePic = './static/chatbot.png'
    if message.split(" ")[0] == '!!':
        name = 'Bot'
        messageSet = ''
        msgArray = re.split("\s", message, 2)

        if msgArray[1] == 'weather':
            try:
                messageSet = Bot(msgArray[2]).getWeather()
            except IndexError as error:
                messageSet = Bot('Please enter city name!!').getWeather()
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet, 'profilePic': './static/chatbot.png'},
                           'totalUsers': len(totalUsers)})
        elif msgArray[1] == 'gif':
            try:
                messageSet = Bot(msgArray[2]).getGif()
            except IndexError as error:
                messageSet = Bot('Please enter valid query!!').getGif()
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': len(totalUsers)})
        elif msgArray[1] == 'help':
            messageSet = 'Working Prefixes: <br>!! about<br>!! weather --City Name' \
                         '<br>!! gif --Query <br> !! funtranslate --String to translate<br>!! randomjoke'
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': len(totalUsers)},
                          room=socketId)
        elif msgArray[1] == 'about':
            messageSet = "Hello! I'm Bot.<br>To learn more about my abilities type: !! help"
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': len(totalUsers)},
                          room=socketId)
        elif msgArray[1] == 'funtranslate':
            try:
                messageSet = Bot(msgArray[2]).funTranslate()
            except IndexError as error:
                messageSet = Bot('Please enter text to translate!!').funTranslate()
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': len(totalUsers)})
        elif msgArray[1] == 'randomjoke':
            messageSet = Bot.genRandomJoke()
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': len(totalUsers)})
        else:
            messageSet = "Command Not Recognized!!"
            socketio.emit('message_sent', {'message': {'name': 'Bot', 'message': messageSet},
                                           'totalUsers': len(totalUsers)})
        db_message = models.Messages(name, messageSet, '', profilePic)
        db.session.add(db_message)
        db.session.commit()
    elif message[:8] == 'https://':
        link = Bot(message).renderLink()
        socketio.emit('message_sent',
                      {'message': {'name': 'Bot', 'message': link,
                                   'profilePic': './static/chatbot.png'}})
        db_message = models.Messages('Bot', link, '', profilePic)
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
    print('Someone connected!')
    socketio.emit('on_connect', {'messages': messagesArray, 'sid': socketId}, room=socketId)

    sockets[socketId] = email
    if email in totalUsers:
        totalUsers[email] += 1
    else:
        totalUsers[email] = 1
    print(sockets)
    print(totalUsers)
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
    print(sockets)
    print(totalUsers)
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
