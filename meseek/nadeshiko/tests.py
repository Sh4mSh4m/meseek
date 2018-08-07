import json
import time 
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from django.test import TestCase, Client, TransactionTestCase, tag
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.test.utils import setup_test_environment
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import UserJapaneseLevel, Hiragana, Katakana
from .tests_data import HIR_char_list
from .quizz import Quizz
from django.test import override_settings


def create_entry_Hiragana(**kwargs):
    """
    Creates a char entry in the tables
    """
    return Hiragana.objects.create(**kwargs)

def create_entry_Katakana(**kwargs):
    """
    Creates a char entry in the tables
    """
    return Katakana.objects.create(**kwargs)

class AwebClientTestCaseNoLogin(TestCase):
    """
    Test suite for the django server, verifying views return expected templates
    """
    def test_index_not_loggedin(self):
        """
        Without being logged in, user has to register or create an account
        """
        response = self.client.get(reverse('nadeshiko:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ecole de langues et cultures japonaises")
        self.assertContains(response, "Enregistrez-vous")
        self.assertContains(response, "inscrivez-vous")

    def test_hiragana_not_loggedin(self):
        """
        Without being logged in, user has to register or create an account
        """
        response = self.client.get(reverse('nadeshiko:hiraganas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hiraganas")

    def test_katakanas_not_loggedin(self):
        """
        Without being logged in, user has to register or create an account
        """
        response = self.client.get(reverse('nadeshiko:katakanas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Katakanas")


class AwebClientTestCaseLoggedIn(TestCase):
    """
    Test suite for the django server, verifying views return expected templates
    and behaviors to get and post requests
    """
    def setUp(self):
        self.user = User.objects.create_user('billy', 'temporary@gmail.com', 'temporary')
        print("The user id is {}".format(self.user.id))
        self.c = Client()
        self.c.login(username="billy", password="temporary")

    def test_1_my_account(self):
        """
        my_acount page loads
        user email appears
        """
        response = self.c.get('/nadeshiko/my_account/1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "temporary@gmail.com")

    def test_2_index_loggedin(self):
        """
        As the user is logged in, user can access quizz
        """
        response = self.c.get(reverse('nadeshiko:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ecole de langues et cultures japonaises")
        self.assertContains(response, "Commencez")

    def test_3_quizz_logged_in_beginner(self):
        """
        Being logged in, username is listed as well with its level
        Newly created user has no score records and starts as beginner
        """
        response = self.c.get(reverse('nadeshiko:quizz'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "billy")
        self.assertContains(response, "niveau 1: débutant")
        self.assertContains(response, "Catégories")
        self.assertContains(response, "Send")

    def test_4_quizz_logged_in_post_initial(self):
        """
        Being logged in, user sends JSON
        Response is JSON with correct Data.
        Question being randomly chosen, it is not tested
        """
        for char in HIR_char_list:
            create_entry_Hiragana(**char)
        MsgClient = {"index": 0,
        "answer": {},
        "reinitRequest": False,
        "settings": {
            "level": 1,
            "quizzLength": 10,
            },
        }
        response = self.c.get(reverse('nadeshiko:quizz'))
        self.assertEqual(response.status_code, 200)
        postresponse = self.c.post(reverse('nadeshiko:quizz'), json.dumps(MsgClient), content_type='application/json')
        self.assertEqual(postresponse.status_code, 200)
        print("le quizzIndex est de : {}".format(postresponse.json()))
        self.assertEqual(postresponse.json()['userInfo']['level'], 1)
        self.assertEqual(postresponse.json()['userInfo']['scores'], {'1': 20, '2': 0})
        self.assertEqual(postresponse.json()['quizzIndex'], 1)
        self.assertEqual(postresponse.json()['quizzLength'], 10)
        self.assertEqual(postresponse.json()['reinitConfirmation'], False)
        self.assertEqual(postresponse.json()['completion'], False)
        self.assertEqual(postresponse.json()['score'], 0)

    def test_5_quizz_logged_in_post_last_answer(self):
        """
        When sending last item, server identifies it is the last question
        and returns that the completion field is True
        """
        for char in HIR_char_list:
            create_entry_Hiragana(**char)
        MsgClient = {"index": 10,
        "answer": {"jp": 'KA', "fr": 'KA'},
        "reinitRequest": False,
        "settings": {
            "level": 1,
            "quizzLength": 10,
            },
        }
        response = self.c.get(reverse('nadeshiko:quizz'))
        self.assertEqual(response.status_code, 200)
        postresponse = self.c.post(reverse('nadeshiko:quizz'), json.dumps(MsgClient), content_type='application/json')
        self.assertEqual(postresponse.status_code, 200)
        self.assertEqual(postresponse.json()['completion'], True)

    def tearDown(self):
        self.user.delete()

class QuizzClass(TestCase):

    @classmethod
    def setUp(self):
        self.user = User.objects.create_user('wally', 'temporary@gmail.com', 'temporary')
        self.userInfo = UserJapaneseLevel.objects.create(pk=self.user.id, user=self.user)
        for char in HIR_char_list:
            create_entry_Hiragana(**char) 

    def test_6_init(self):
        """
        With data populated in database and with newly created user
        Test quizz object initialization
        Questions dict content is not tested as populated randomly but tested and not empty with 10 items
        """
        quizz = Quizz(self.user)
        self.assertEqual( quizz.user, self.user)
        self.assertEqual( quizz.userInfo, self.userInfo)
        self.assertEqual( quizz.user, self.user)
        self.assertEqual( quizz.scoreSheet, {1: 20, 2: 0})
        self.assertEqual( len(quizz.questions), 10)
        self.assertEqual( len(quizz.answers), 10)
        self.assertEqual( quizz.answers[1], {})
        self.assertEqual( quizz.level, 1)
        self.assertEqual( quizz.size, 10)
        self.assertEqual( quizz.categories, ['hiraganas'])
        self.assertEqual( quizz.currentScore, 0)
        self.assertEqual( quizz.completed, False)

    def test_6_currentIndex(self):
        """
        Quizz method returns non empty answers dict max key and adds 1 
        """
        quizz = Quizz(self.user)
        quizz.answers = {1: {1:1}, 2:{}, 3:{}}
        quizz.index = quizz.currentIndex()
        self.assertEqual ( quizz.index, 2)

    def test_6_updatesData(self):
        """
        Quizz method updates index and answers dict
        """
        quizz = Quizz(self.user)
        dataJSON= {
            'index': 2,
            'answer': {"jp": 'KA', "fr": 'KA'},
            }
        quizz.updatesData(dataJSON)
        self.assertEqual( quizz.index, 3)

    def test_6_updatesDataCompleted(self):
        """
        Based on quizz size, if last answer comes in
        completion bit is set to 1
        """
        quizz = Quizz(self.user)
        quizz.size = 2
        dataJSON= {
            'index': 2,
            'answer': {"jp": 'KA', "fr": 'KA'},
            }
        quizz.updatesData(dataJSON)
        self.assertEqual( quizz.completed, True)

    def test_6_assesesScore(self):
        """
        Quizz asseses score based on Quizz questions and answers
        Score is updated by 1 for each matching key value in questions and answers of the quizz
        Score is an integer with a base of 100 and resets index to 1
        """
        quizz = Quizz(self.user)
        quizz.size = 2
        quizz.questions = {1:1, 2:2}
        quizz.answers = {1:1, 2:3}
        quizz.assesesScore()
        self.assertEqual(quizz.currentScore, 50)
        self.assertEqual(quizz.index, 1)

    def test_6_recordsScore(self):
        """
        with quizz calculated score, methods updates User score in database by removing last entry and updating first.
        Default score sheet is 0-0-0-0-1
        """
        quizz = Quizz(self.user)
        quizz.level = 1
        quizz.currentScore = 90
        quizz.recordsScore()
        score_sheets = UserJapaneseLevel.objects.get(pk=self.user.id)
        self.assertEqual(score_sheets.scores_level1, '0.9-0-0-0-0')


    def test_6_recordsScoreAndLevelUp(self):
        """
        As current score is recorded. Method must evaluate is average score or user for that level is above 90 percent. If so, it records default score for next level
        """
        quizz = Quizz(self.user)
        quizz.level = 1
        quizz.userInfo.scores_level1 = '1-1-1-1-1'
        quizz.currentScore = 90
        quizz.recordsScore()
        score_sheets = UserJapaneseLevel.objects.get(pk=self.user.id)
        self.assertEqual(score_sheets.scores_level1, '0.9-1-1-1-1')
        self.assertEqual(score_sheets.scores_level2, '0-0-0-0-1')
        
    
class seleniumTestsNotLoggedIn(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @tag('sel')
    def test_index_no_login(self):
        """
        Integration test, verify presence of register icon in page
        Link to register to accounts/login
        Link to signup
        Verify section about is present
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/nadeshiko/'))
        self.selenium.find_element_by_xpath('//i[@class="fa fa-users fa-2x"]')
        self.selenium.find_element_by_xpath('//a[contains(@href,"nadeshiko/accounts/login")]')
        self.selenium.find_element_by_xpath('//a[contains(@href,"signup")]')
        self.selenium.find_element_by_xpath('//section[@id="about"]')

    @tag('sel')
    def test_signup_no_login(self):
        """
        Signup form containing the various fields required for signup         """
        self.selenium.get('%s%s' % (self.live_server_url, '/signup/'))
        self.selenium.find_element_by_xpath('//input[contains(@name, "username")]')
        self.selenium.find_element_by_xpath('//input[contains(@name, "first_name")]')
        self.selenium.find_element_by_xpath('//input[contains(@name, "last_name")]')
        self.selenium.find_element_by_xpath('//input[contains(@name, "email")]')
        self.selenium.find_element_by_xpath('//input[contains(@name, "password1")]')
        self.selenium.find_element_by_xpath('//input[contains(@name, "password2")]')

    @tag('sel')
    def test_register(self):

        """
        Signup form containing the various fields required for signup
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/nadeshiko/accounts/login/'))
        self.selenium.find_element_by_xpath('//input[contains(@name,"username")]')
        self.selenium.find_element_by_xpath('//input[contains(@name,"password")]')

@override_settings(DEBUG=True)
class seleniumTestsLoggedIn(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.user = User.objects.create_user('wally', 'temporary@gmail.com', 'temporary')
        cls.userInfo = UserJapaneseLevel.objects.create(pk=cls.user.id, user=cls.user)
        for char in HIR_char_list:
            create_entry_Hiragana(**char) 

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @tag('last')
    def test_index_loggedin(self):
        """
        Integration test, 
        user logs in, 
        icons in top nav bar change
        user can access quizz
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/nadeshiko/'))
        #user logs in
        self.selenium.find_element_by_xpath('//a[contains(@href, "login")]').click()
        self.selenium.find_element_by_xpath('//input[contains(@name, "username")]').send_keys('wally')
        self.selenium.find_element_by_xpath('//input[contains(@name, "password")]').send_keys('temporary')
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        # Users returns to index page but clicks starts here
        self.selenium.find_element_by_xpath('//a[contains(@href, "quizz")]').click()
        # Page loads with username displayed
        self.selenium.find_element_by_xpath('//h4[contains(text(), "wally")]')
        # Quizz init
        self.selenium.execute_script("")
        self.selenium.find_element_by_xpath('//form[@id="theForm"]').submit()
        # Quizz starts with question 1/10
        #self.selenium.find_element_by_xpath('//div[@id="questionProgression"]')
