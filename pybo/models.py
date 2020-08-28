from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    #외래키 추가
    #특정사용자가 작성한 질문 cur_user.author_question.all()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #추천 User모델과 다대다관계
    #특정사용자가 투표한 질문 cur_user.voter_question.all()
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):
        return self.subject

class Answer(models.Model):
    #Question을 외래키로 가짐.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    voter = models.ManyToManyField(User, related_name='voter_answer')

    def __str__(self):
        return self.content

#댓글기능을 위한 모델
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question,null=True,blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer,null=True,blank=True,on_delete=models.CASCADE)
    #방명록기능을 위해 추가
    user = models.ManyToManyField(User,related_name='user_comment')
