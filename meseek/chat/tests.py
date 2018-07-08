import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Rappel
from .f_parser.parser import arraySentencesCleaner, msgParser

linux = {
    'id': 1,
    'name': "linux",
    'rappel': "Vraiment !\r\nhello" 
}

def createsRappel(**kwargs):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    return Rappel.objects.create(**kwargs)

class TestParser(TestCase):
    def setUp(self):
        self.array = [" hello", "bye ", " word "]
        self.msg = """La phrase1 avec stuff. Une phrase2, mais du stuff. La blabla et la question1 ? Le blabla et sa question2 ? Une phrase3 and more."""

    
    def test_arraySentencesCleaner(self):
        parsed = arraySentencesCleaner(self.array)
        result = ["hello", "bye", "word"]
        self.assertEqual(parsed, result)


    def test_parser(self):
        """
        parses correctly the rawIput
        """
        resultS = ['la phrase1 avec stuff', 'une phrase2', 'mais du stuff', 'une phrase3 and more']
        resultQ = ['la blabla et la question1', 'le blabla et sa question2']
        response = msgParser(self.msg) 
        self.assertEqual(response['sentences'], resultS)
        self.assertEqual(response['questions'], resultQ)

class webClientTestCase(TestCase):
    """
    Test suite for the django server, verifying it builds up the 
    index.html page on get requests and that the input container 
    is present
    """
    @classmethod
    def setUp(cls):
        #cls.driver = webdriver.Chrome()
        rappel = createsRappel(**linux)

    def test_index_no_login(self):
        """
        If no login, response OK.
        """
        response = self.client.get(reverse('chat:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I'm Mister Meseek")

    def test_chatterbot_dialog(self):
        json_data = json.dumps({'userId': 1, 'rawInput' : 'Ca va mec'})
        response = self.client.post(reverse('chat:index'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "OKLM")

    def test_rappel(self):
        json_data = json.dumps({'userId': 1, 'rawInput' : '/r linux'})
        response = self.client.post(reverse('chat:index'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vraiment")
        self.assertContains(response, "ello")


    @classmethod
    def tearDown(cls):
        #cls.driver.quit()
        pass