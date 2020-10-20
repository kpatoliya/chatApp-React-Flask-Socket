import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API')
GIPHY_API_KEY = os.getenv('GIPHY_API')


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
        return "<h4> <img src='" + self.string + "' width='250' height='250'> </h4>"

    @staticmethod
    def genRandomJoke():
        content = json.loads(requests.get('https://sv443.net/jokeapi/v2/joke/Programming?type=single').text)
        return content['joke']
