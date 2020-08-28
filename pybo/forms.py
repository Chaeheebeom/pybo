from django import forms
from pybo.models import Question, Answer, Comment

#모델폼은 모델과 연결된 폼이다.
#아래모델의 경우 Question모델의 데이터를 저장할 수 있다.
#모델폼의 경우 내부클래스인 Meta가 반드시 있어야 한다.
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        #속성설정.
        fields =['subject','content']
        #widgets={
        #    'subject':forms.TextInput(attrs={'class':'form-control'}),
        #    'content':forms.Textarea(attrs={'class':'form-control','rows':10}),
        #}
        labels={
            'subject':'제목',
            'content':'내용',
        }
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content':'답변내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }