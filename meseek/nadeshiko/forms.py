from django import forms
from .models import LessonScan

class QuizzConfigurationForm(forms.Form):
    SIZE=[(10,'Standard'),
         (20,'Medium')]
    Difficulté = forms.ChoiceField(choices=SIZE, widget=forms.RadioSelect(attrs={'style': 'display: inline'}))

class LessonScanForm(forms.ModelForm):
    class Meta:
        model = LessonScan
        fields = ('description', 'image', )




class OCRTextForm(forms.Form):
    VOCTYPE=[('vocabulaire','Vocabulaire'),
         ('other', 'Other')]
    Type = forms.ChoiceField(choices=VOCTYPE, widget=forms.RadioSelect(attrs={'style': 'display: inline-block'}))
    Level = forms.IntegerField(initial=3, required=True)
    
    def __init__(self, *args, **kwargs):
        wordList = kwargs.pop('wordList')
        super(OCRTextForm, self).__init__(*args, **kwargs)
        if wordList:
            for word in wordList:
                self.fields['Mot{}'.format(wordList.index(word))]=forms.CharField(initial=word, required=False)
