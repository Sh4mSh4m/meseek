from django.test import TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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


class webClientTestCase(TestCase):
    """
    Test suite for the django server, verifying it builds up the 
    index.html page on get requests and that the input container 
    is present
    """
    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome()

    def test_webpage_loads(self):
        """
        Client opens up a firefox, types in the URL and checks that
        this is the right website
        """
        driver = self.driver
        self.driver.get('http://localhost:8000/chat')
        test = driver.find_element_by_id("global")
        # test = driver.find_element_by_xpath("//p[@id='global']")
        self.assertIn("Welcome", test.text)
        # self.assertIn("Rick'n'Morty's multiverse locator", driver.title)#

    def test_webpage_input(self):
        """
        Client opens up a firefox, locates the input field, enter text.
        text appears in the display area
        """
        driver = self.driver
        self.driver.get('http://localhost:8000/chat')
        chat_input = driver.find_element_by_xpath("//textarea[@id='dialogInput']")
        chat_input.clear()
        chat_input.send_keys('some text')
        chat_input.send_keys(Keys.RETURN)
        chat_area = driver.find_element_by_id("dialogDisplay")
        self.assertIn("some text", chat_area.text)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()