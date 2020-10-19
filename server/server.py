import json
import os
import re
import flask
import requests
from flask import render_template, request
from flask_socketio import SocketIO
from dotenv import load_dotenv
from random_username.generate import generate_username
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
totalUsers = 0


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
        return "<h4> <img src='" + giphy + "'> </h4>"

    def funTranslate(self):
        if self.string == 'Please enter text to translate!!':
            return self.string
        content = json.loads(requests.get('https://api.funtranslations.com/translate/emoji.json?text='
                                          + self.string).text)
        retString = content['contents']['translated']
        return retString

    @staticmethod
    def genRandomJoke():
        content = json.loads(requests.get('https://sv443.net/jokeapi/v2/joke/Programming?type=single').text)
        return content['joke']


@socketio.on('message')
def handle_message(msg):
    global totalUsers
    socketId = request.sid
    db_message = models.Messages(msg['name'], msg['message'])
    db.session.add(db_message)
    db.session.commit()

    message = msg['message'].strip()

    if message.split(" ")[0] == '!!':
        name = 'Bot'
        messageSet = ''
        socketio.emit('message_sent', {'message': msg, 'totalUsers': totalUsers})
        msgArray = re.split("\s", message, 2)

        if msgArray[1] == 'weather':
            try:
                messageSet = Bot(msgArray[2]).getWeather()
            except IndexError as error:
                messageSet = Bot('Please enter city name!!').getWeather()
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': totalUsers})
        elif msgArray[1] == 'gif':
            try:
                messageSet = Bot(msgArray[2]).getGif()
            except IndexError as error:
                messageSet = Bot('Please enter valid query!!').getGif()
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': totalUsers})
        elif msgArray[1] == 'help':
            messageSet = 'Working Prefixes: <br>!! about<br>!! weather --City Name' \
                          '<br>!! gif --Query <br> !! funtranslate --String to translate<br>!! randomjoke'
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': totalUsers},
                          room=socketId)
        elif msgArray[1] == 'about':
            messageSet = "Hello! I'm Bot.<br>To learn more about my abilities type: !! help"
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': totalUsers},
                          room=socketId)
        elif msgArray[1] == 'funtranslate':
            try:
                messageSet = Bot(msgArray[2]).funTranslate()
            except IndexError as error:
                messageSet = Bot('Please enter text to translate!!').funTranslate()
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': totalUsers})
        elif msgArray[1] == 'randomjoke':
            messageSet = Bot.genRandomJoke()
            socketio.emit('message_sent',
                          {'message': {'name': 'Bot', 'message': messageSet}, 'totalUsers': totalUsers})
        else:
            messageSet = "Command Not Recognized!!"
            socketio.emit('message_sent', {'message':  {'name': 'Bot', 'message': messageSet},
                                           'totalUsers': totalUsers})
        db_message = models.Messages(name, messageSet)
        db.session.add(db_message)
        db.session.commit()
    else:
        socketio.emit('message_sent', {'message': msg, 'totalUsers': totalUsers})


@socketio.on('connect')
def on_connect():
    global totalUsers
    messagesArray = []
    all_messages = db.session.query(models.Messages).all()
    for message in all_messages:
        messagesArray.append({"name": message.user_name, "message": message.text})
    userName = generate_username()[0]
    socketId = request.sid
    totalUsers += 1
    print('Someone connected!')
    socketio.emit('on_connect', {'totalUsers': totalUsers, 'userName': userName, 'messages': messagesArray},
                  room=socketId)
    socketio.emit('update_users', {'totalUsers': totalUsers})


@socketio.on('disconnect')
def on_disconnect():
    global totalUsers
    totalUsers -= 1
    print('Someone disconnected!')
    socketio.emit('on_disconnect', {'totalUsers': totalUsers})


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
