from math import ceil
from .models import Hiragana, Katakana, UserJapaneseLevel

class Quizz():
    """
    Quizz class associated to users id and stored in a dictionnary
    for follow up
    """

    def __init__(self, user):
        self.user = user
        try:
            userInfo = UserJapaneseLevel.objects.get(pk=self.user.id)
        except UserJapaneseLevel.DoesNotExist:
            userInfo = UserJapaneseLevel.objects.create(pk=self.user.id, user=self.user)
        finally:
            self.scoreSheet = self.asseses(userInfo)
            self.level = max([ x for x in self.scoreSheet.keys() if self.scoreSheet[x] != 0])
            # updatable per methods
            self.size = 10
            self.categories = self.listsCategories()
            self.questions = self.populatesQuestions()
            self.answers = self.populatesAnswers()
            self.index = self.currentIndex()

    def asseses(self, UserJapaneseLevelObject):
        scoreSheet = {}
        for i in range(1,4):
            scores_level = "scores_level{}".format(i)
            scores = getattr(UserJapaneseLevelObject, scores_level)
            scoresList = scores.split("-")
            scores = [ int(x) for x in scoresList]
            scoreSheet[i] = (sum(scores)/len(scores))
        return scoreSheet

    def listsCategories(self):
        if self.level == 1:
            return ['hiraganas']
        if self.level == 2:
            return ['katakanas']
        if self.level == 3: 
            return ['hiraganas', 'katakanas']

    def populatesQuestions(self):
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
        answersDict = {}
        for index in self.questions.keys():
            answersDict[index] = {}
        return answersDict
         
    def currentIndex(self):
        try:
            index = max([ x for x in self.answers.keys() if self.answers[x] != {} ]) + 1
        except ValueError:
            index = 1
        finally:
            return index

    def levelUp(self):
        pass



#var MsgClient = {
#    "answer": Caca,
#    "reinitRequest": False,
#    "settings": {
#        "level": 1,
#        "quizzLength": 10,
#        }
#    }

#{
#    "userInfo":
#        {
#        "level": Integer
#        "scores": Dict
#        }
#    "quizzIndex": ""
#    "quizzQuestion": ""
#    "quizzLength": integer
#    "reinitConfirmation": Boolean
#    "completion": Boolean
#    "score": Integer
#}
