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

    @tag('staff')
    def test_upload(self):
        """
        Without being logged in, or user not staff
        """
        response = self.client.get(reverse('nadeshiko:upload'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, this is a staff page only")



class AwebClientTestCaseLoggedIn(TestCase):
    """
    Test suite for the django server, verifying views return expected templates
    and behaviors to get and post requests
    """
    def setUp(self):
        self.user = User.objects.create_user('billy', 'temporary@gmail.com', 'temporary')
        self.c = Client()
        self.c.login(username="billy", password="temporary")

    def test_1_my_account(self):
        """
        my_acount page loads
        user email appears
        """
        response = self.c.get('/nadeshiko/my_account/{}'.format(self.user.id))
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
        self.assertContains(response, "Configuration")
        self.assertContains(response, "Difficulté")
        self.assertContains(response, "Standard")        
        self.assertContains(response, "Send")

    def test_4_quizz_logged_in_post_initial(self):
        """
        Being logged in, user sends JSON
        Response is JSON with correct Data.
        Question being randomly chosen, it is not tested, neither is answer
        """
        for char in HIR_char_list:
            create_entry_Hiragana(**char)
        MsgClient = {"index": 1,
        "answer": {"jp": 'ju', "fr": 'ju'},
        }
        kwargs_user = {'user_id': self.user.id}
        response = self.c.get('/nadeshiko/quizz/{}'.format(self.user.id))
        self.assertEqual(response.status_code, 200)
        postresponse = self.c.post('/nadeshiko/quizz/{}'.format(self.user.id), json.dumps(MsgClient), content_type='application/json')
        self.assertEqual(postresponse.status_code, 200)
        self.assertEqual(postresponse.json()['userInfo']['level'], 1)
        self.assertEqual(postresponse.json()['userInfo']['scores'], {'1': 20, '2': 0})
        self.assertEqual(postresponse.json()['quizzIndex'], 2)
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
        }
        response = self.c.get('/nadeshiko/quizz/{}'.format(self.user.id))
        self.assertEqual(response.status_code, 200)
        postresponse = self.c.post('/nadeshiko/quizz/{}'.format(self.user.id), json.dumps(MsgClient), content_type='application/json')
        self.assertEqual(postresponse.status_code, 200)
        self.assertEqual(postresponse.json()['completion'], True)

    def tearDown(self):
        self.user.delete()


class StaffFeatures(TestCase):
    """
    Test suite for the django server, verifying views return expected templates
    and behaviors to get and post requests
    """
    def setUp(self):
        self.user = User.objects.create_user('staff', 'temporary@gmail.com', 'temporary')
        self.user.is_staff = True
        self.user.save()
        self.c = Client()
        self.c.login(username="staff", password="temporary")

    @tag('staff')
    def test_staff_upload(self):
        """
        As the user is logged in, user can access quizz
        """
        response = self.c.get(reverse('nadeshiko:upload'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload")

    def tearDown(self):
        self.user.delete()


