from math import ceil, floor
from .models import Hiragana, Katakana, UserJapaneseLevel
from django import forms
from django.utils.safestring import mark_safe


class QuizzConfigurationForm(forms.Form):
    SIZE=[(10,'Standard'),
         (20,'Medium')]
    Difficulté = forms.ChoiceField(choices=SIZE, widget=forms.RadioSelect(attrs={'style': 'display: inline'}))

class OCRTextForm(forms.Form):
    def __init__(self, wordList):
        super().__init__()
        for word in wordList:
            self.fields['word{}'.format(wordList.index(word))]=forms.CharField(initial=word)

class Quizz():
    """
    Quizz class associated to users id and stored in a dictionnary
    for follow up
    """
    MAX_LEVEL = 2

    def __init__(self, user):
        """
        Initializes every quizz attribute
        """
        # For initialization
        self.user = user
        self.userInfo = self.collectsUserInfo()
        self.scoreSheet = self.assesesScoreSheet()
        self.level = self.assesesLevel()
        self.index = 1
        self.currentScore = 0
        # Per user setup
        self.size = 10
        self.categories = self.listsCategories()
        self.questions = self.populatesQuestions()
        self.answers = self.populatesAnswers()
        # Bits modified per method
        self.completed = False
        self.lastAnswer = None

    def collectsUserInfo(self):
        """
        Queries users database info
        """
        try:
            userInfo = UserJapaneseLevel.objects.get(pk=self.user.id)
        except UserJapaneseLevel.DoesNotExist:
            userInfo = UserJapaneseLevel.objects.create(pk=self.user.id, user=self.user)
        finally:
            return userInfo

    def assesesScoreSheet(self):
        """
        Fetches users score sheet from database, returns dict
        """
        scoreSheet = {}
        for i in range(1, self.MAX_LEVEL+1):
            scores_level = "scores_level{}".format(i)
            scores = getattr(self.userInfo, scores_level)
            scoresList = scores.split("-")
            scoreSheet[i] = self.averagesList(scoresList)
        return scoreSheet

    def assesesLevel(self):
        """
        Returns users level based on their scoreSheet
        """
        level = max([ x for x in self.scoreSheet.keys() if self.scoreSheet[x] != 0])
        return level

    def listsCategories(self):
        """
        Returns categories list depending on quizz level
        """
        if self.level == 1:
            return ['hiraganas']
        if self.level == 2:
            return ['katakanas']
        if self.level == 3: 
            return ['hiraganas', 'katakanas']

    def populatesQuestions(self):
        """
        Queries database for items to quizz about, returns dict
        """
        questionsDict = {}
        index = 1
        if self.level == 1:
            questions = Hiragana.objects.order_by('?')[:self.size]
        if self.level == 2:
            questions = Katakana.objects.order_by('?')[:self.size]            
#        if self.level == 3: 
#            nbPerCategories = ceil(self.size/len(self.categories))
        for question in questions:
            questionsDict[index] = {"jp":question.char_jp, "fr":question.char_fr}
            index += 1
        return questionsDict

    def populatesAnswers(self):
        """
        Creates the answer dict based on number of entries in questions dict
        """
        answersDict = {}
        for index in self.questions.keys():
            answersDict[index] = {}
        return answersDict
         
    def currentIndex(self):
        """
        Defines index to quizz user about based on answer dict sheet
        """
        try:
            index = max([ x for x in self.answers.keys() if self.answers[x] != {} ]) + 1
        except ValueError:
            index = 1
        finally:
            return index

    def updatesData(self, dataJSON):
        """
        Fills in answer sheet, and if reached end of questions list, 
        evaluates currentScore and indicates that quizz is over
        Index is updated here
        """
        answerIndex = dataJSON['index']
        self.answers[answerIndex] = dataJSON['answer']
        self.lastAnswer = self.assesesLastAnswer()
        self.index = self.currentIndex()
        if self.index == self.size + 1:
            # resets some quizz data including index so that MsgServer can be sent
            self.index = 1
            self.assesesScore()
            self.recordsScore()
            # This will trigger quizz reinitialization on next Ajax post request
            self.completed = True

    def assesesLastAnswer(self):
        lastIndex = self.index
        if self.questions[lastIndex] == self.answers[lastIndex]:
            return True
        else:
            return False

    def assesesScore(self):
        """
        Based on questions and answers, evaluates current score 
        """
        goodAnswers = 0
        for index in self.questions.keys():
            if self.questions[index] == self.answers[index]:
                goodAnswers += 1
        self.currentScore = floor((goodAnswers/self.size)*100)

    def recordsScore(self):
        """
        Removes oldest score entry
        Updates it with currentScore
        Evlauates level up or not
        Updates users scoreSheet in the database
        """
        scores_level = "scores_level{}".format(self.level)
        currentScoreSheet = getattr(self.userInfo, scores_level)
        scoresList = currentScoreSheet.split("-")
        scoresList.pop()
        scoresList.insert(0, str(self.currentScore/100))
        # Evaluates level up
        if (self.averagesList(scoresList) >= 90) and (self.level < self.MAX_LEVEL) :
            next_score_level = "scores_level{}".format(self.level+1)
            new_field_kwarg = {next_score_level: "0-0-0-0-1"}
            UserJapaneseLevel.objects.filter(pk=self.user.id).update(**new_field_kwarg)
        newScoreSheet = '-'.join(scoresList)
        field_kwarg = {scores_level: newScoreSheet}
        UserJapaneseLevel.objects.filter(pk=self.user.id).update(**field_kwarg)
        check = UserJapaneseLevel.objects.get(pk=self.user.id)

    def averagesList(self, aList):
        nList = [ float(x) for x in aList]
        return floor((sum(nList)/len(nList))*100)
        