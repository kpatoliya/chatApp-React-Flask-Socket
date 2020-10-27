import unittest
from bot import Bot
import models


class UnmockedTestCase(unittest.TestCase):
    def setUp(self):
        self.user = models.Messages('karan', 'test message', 'karan@gmail.com', 'profilepic.com')

    def test_models_init(self):
        user = self.user
        self.assertEqual(user.user_name, 'karan')
        self.assertEqual(user.text, 'test message')
        self.assertEqual(user.email, 'karan@gmail.com')
        self.assertEqual(user.profilePic, 'profilepic.com')

    def test_models_repr(self):
        expected = str({
            'userId': 'karan',
            'body': 'test message',
            'email': 'karan@gmail.com',
            'profilePic': 'profilepic.com'
        })
        self.assertEqual(self.user.__repr__(), expected)

    def test_bot_help(self):
        expected = 'Working Prefixes: <br>!! about<br>!! weather --City Name' \
                   '<br>!! gif --Query <br> !! funtranslate --String to translate<br>!! randomjoke'
        self.assertEqual(Bot.botHelp(), expected)

    def test_bot_about(self):
        expected = "Hello! I'm Bot.<br>To learn more about my abilities type:<br>!! help"
        self.assertEqual(Bot.botAbout(), expected)

    def test_bot_renderImage(self):
        expected = "<h4> <img src='" + 'https://www.picture.jpg' + "' width='250' height='250'> </h4>"
        self.assertEqual(Bot('https://www.picture.jpg').renderImage(), expected)

    def test_bot_renderLink(self):
        message = 'https://www.picture.com'
        expected = "<u> <a href='" + message + "'>" + message + "</a></u>"
        self.assertEqual(Bot('https://www.picture.com').renderLink(), expected)

    def test_bot_get_weather_error(self):
        expected = 'Please enter city name!!'
        self.assertEqual(Bot('Please enter city name!!').getWeather(), expected)

    def test_bot_get_gif_error(self):
        expected = 'Please enter valid query!!'
        self.assertEqual(Bot('Please enter valid query!!').getGif(), expected)

    def test_bot_get_funtranslate_error(self):
        expected = 'Please enter text to translate!!'
        self.assertEqual(Bot('Please enter text to translate!!').funTranslate(), expected)

    def test_bot_invalid_bot_command(self):
        expected = 'Command Not Recognized!!'
        self.assertEqual(Bot.botCommandInvalid(), expected)


if __name__ == '__main__':
    unittest.main()
