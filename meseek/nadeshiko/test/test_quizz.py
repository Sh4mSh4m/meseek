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
        
    
