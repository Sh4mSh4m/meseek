from django.test import TestCase
from django.urls import reverse
from .f_parser.parser import arraySentencesCleaner, msgParser
# Create your tests here.

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


class TestChat(TestCase):
    def test_index_no_login(self):
        """
        If no login, response OK.
        """
        response = self.client.get(reverse('chat:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to MeSeek bot v2.0")