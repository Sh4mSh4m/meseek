import json
import time
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from django.test import TestCase, Client, TransactionTestCase, tag
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.test.utils import setup_test_environment
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.test import override_settings
from ..models import UserJapaneseLevel, Hiragana, Katakana
from ..quizz import Quizz
from .tests_data import HIR_char_list


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

    @tag('selenium')
    def test_1_sel_index_no_login(self):
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

    @tag('selenium')
    def test_2_sel_signup_no_login(self):
        """
        Signup form containing the various fields required for signup         """
        self.selenium.get('%s%s' % (self.live_server_url, '/signup/'))
        self.selenium.find_element_by_xpath('//input[contains(@name, "username")]')
        self.selenium.find_element_by_xpath('//input[contains(@name, "first_name")]')
        self.selenium.find_element_by_xpath('//input[contains(@name, "last_name")]')
        self.selenium.find_element_by_xpath('//input[contains(@name, "email")]')
        self.selenium.find_element_by_xpath('//input[contains(@name, "password1")]')
        self.selenium.find_element_by_xpath('//input[contains(@name, "password2")]')

    @tag('selenium')
    def test_3_sel_register(self):

        """
        Signup form containing the various fields required for signup
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/nadeshiko/accounts/login/'))
        self.selenium.find_element_by_xpath('//input[contains(@name,"username")]')
        self.selenium.find_element_by_xpath('//input[contains(@name,"password")]')

#@override_settings(DEBUG=True)
class seleniumTestsLoggedIn(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(15)
        cls.user = User.objects.create_user('wally', 'temporary@gmail.com', 'temporary')
        cls.staff = User.objects.create_user('staff', 'temporary@gmail.com', 'temporary')
        cls.staff.is_staff = True
        cls.staff.save()
        cls.userInfo = UserJapaneseLevel.objects.create(pk=cls.user.id, user=cls.user)
        for char in HIR_char_list:
            create_entry_Hiragana(**char)


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    @tag('selenium', 'solo')
    def test_sel_index_loggedin(self):
        """
        Integration test, 
        user logs in, 
        user can access quizz
        user answers 5 questions
        user leaves
        user comes back and can pursue his quizz
        Server informs user successfully finished quizz
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/nadeshiko/'))
        #user logs in
        self.selenium.find_element_by_xpath('//a[contains(@href, "login")]').click()
        self.selenium.find_element_by_xpath('//input[contains(@name, "username")]').send_keys('wally')
        self.selenium.find_element_by_xpath('//input[contains(@name, "password")]').send_keys('temporary')
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        # Users returns to index page but clicks starts here
        # Page loads with username displayed
        self.selenium.find_element_by_xpath('//h4[contains(text(), "wally")]')
        # Quizz init
        self.selenium.find_element_by_xpath('//form[@id="theForm"]').submit()
        # Quizz starts with question 1/10
        self.selenium.find_element_by_xpath('//h4[contains(text(), "vous de jouer")]')
        for i in range(1,6):
            self.selenium.find_element_by_xpath('//div[@id="questionProgression" and contains(text(), "Question: {}")]'.format(i))
            self.selenium.find_element_by_xpath('//input[@id="answerInput"]').send_keys("ku")
            self.selenium.find_element_by_xpath('//input[@id="answerInput"]').send_keys(Keys.RETURN)
        # User goes back to quizz page
        self.selenium.get('%s%s' % (self.live_server_url, '/nadeshiko/quizz'))
        # User finds link to continue
        self.selenium.find_element_by_xpath('//a[contains(text(), "finissez-le")]').click()
        for i in range(6,11):
            self.selenium.find_element_by_xpath('//div[@id="questionProgression" and contains(text(), "Question: {}")]'.format(i))
            self.selenium.find_element_by_xpath('//input[@id="answerInput"]').send_keys("ku")
            self.selenium.find_element_by_xpath('//input[@id="answerInput"]').send_keys(Keys.RETURN)
        self.selenium.find_element_by_xpath('//h4[contains(text(), "Vous avez terminé")]')




#@override_settings(DEBUG=True)
class seleniumTestsStaff(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(15)
        cls.user = User.objects.create_user('wally', 'temporary@gmail.com', 'temporary')
        cls.staff = User.objects.create_user('staff', 'temporary@gmail.com', 'temporary')
        cls.staff.is_staff = True
        cls.staff.save()
        cls.userInfo = UserJapaneseLevel.objects.create(pk=cls.user.id, user=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    @tag('selenium', 'staff', 'zetest')
    def test_sel_staff_upload(self):
        """
        Integration test, 
        user logs in, 
        user can access quizz
        user answers 10 questions
        Server informs user successfully finished quizz
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/nadeshiko/'))
        # staff logs in
        self.selenium.find_element_by_xpath('//a[contains(@href, "login")]').click()
        self.selenium.find_element_by_xpath('//input[contains(@name, "username")]').send_keys('staff')
        self.selenium.find_element_by_xpath('//input[contains(@name, "password")]').send_keys('temporary')
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        # staff goes to upload page
        self.selenium.get('%s%s' % (self.live_server_url, '/nadeshiko/upload'))
        self.selenium.find_element_by_xpath('//strong[contains(text(), "upload de scans")]')
        # Staff selects an image to load
        self.selenium.find_element_by_xpath('//input[@id="id_image"]').send_keys(os.getcwd()+"/test-Lesson1-1.png")
        # Sending scan
        self.selenium.find_element_by_xpath('//button[contains(text(), "Upload du scan")]').click()
        # Scan is sent and user is informed the page is loading
        self.selenium.find_element_by_xpath('//div[contains(text(), "Votre scan est en cours de chargement")]')
        # Form is returned and an image is loaded
        self.selenium.find_element_by_xpath('//p[contains(text(), "Le fichier a bien été chargé")]')
        # Staff fills in fields
        # Default type is selected now
        self.selenium.find_element_by_xpath('//input[@id="id_Type_0"]').click()
        self.selenium.find_element_by_xpath('//input[@id="id_Mot0"]').clear()
        self.selenium.find_element_by_xpath('//input[@id="id_Mot0"]').send_keys("わたし//je")
        self.selenium.find_element_by_xpath('//input[@id="id_Mot1"]').clear()
        self.selenium.find_element_by_xpath('//input[@id="id_Mot1"]').send_keys("あなた//vous")
        self.selenium.find_element_by_xpath('//input[@id="id_Mot2"]').clear()
        self.selenium.find_element_by_xpath('//input[@id="id_Mot2"]').send_keys("あの ひど//il")
        # Staff sends form
        self.selenium.find_element_by_xpath('//button[contains(text(), "Upload")]').click()
        # Staff is confirmed of words he added
        self.selenium.find_element_by_xpath('//li[contains(text(), "わたし")]')


