import unittest
import unittest.mock as mock
from bot import Bot
from flask import render_template, request
import models
from server import socketio, app, sockets, totalUsers, handle_message, addToDb, update_users, on_disconnect


class MockedDbQuery:
    def __init__(self, user_name, text, profilePic):
        self.user_name = user_name
        self.text = text
        self.profilePic = profilePic


class MockedMessage:
    def __init__(self, name, message, email, profilePic):
        self.name = name
        self.message = message
        self.email = email
        self.profilePic = profilePic


class MockedTestCase(unittest.TestCase):

    def test_bot_getWeather(self):
        with mock.patch('json.loads') as mock_search:
            mock_search.return_value = {
                "weather": [{
                    "description": "mist",
                    "icon": "50d"
                }],
                "main": {
                    "temp": 54.52,
                },
                "cod": 200
            }
            expected = "<h4>clifton: 54.52°F<img src='http://openweathermap.org/img/w/50d.png'>mist</h4>"
            self.assertEqual(Bot('clifton').getWeather(), expected)
        with mock.patch('json.loads') as mock_search:
            mock_search.return_value = {
                "cod": 400}
            expected = "Invalid Input!!"
            self.assertEqual(Bot('random').getWeather(), expected)

    def test_bot_getGif(self):
        with mock.patch('json.loads') as mock_search:
            mock_search.return_value = {
                "data": [{
                    "images": {
                        "downsized": {
                            "url": 'https://www.gif.com'
                        }
                    }
                }],
                "pagination": {
                    "total_count": 2
                }
            }
            expected = "<h4> <img src='https://www.gif.com' width='250' height='250'> </h4>"
            self.assertEqual(Bot('random').getGif(), expected)
        with mock.patch('json.loads') as mock_search:
            mock_search.return_value = {
                "pagination": {
                    "total_count": 0
                }
            }
            expected = "Invalid Input!!"
            self.assertEqual(Bot('random').getGif(), expected)

    def test_bot_funTranslate(self):
        with mock.patch('json.loads') as mock_search:
            mock_search.return_value = {
                "contents": {
                    "translated": 'This is translated message'
                }
            }
            expected = "This is translated message"
            self.assertEqual(Bot('random').funTranslate(), expected)

    def test_bot_genRandomJoke(self):
        with mock.patch('json.loads') as mock_search:
            mock_search.return_value = {
                "joke": 'generated random joke'
            }
            expected = "generated random joke"
            self.assertEqual(Bot.genRandomJoke(), expected)


if __name__ == '__main__':
    unittest.main()
