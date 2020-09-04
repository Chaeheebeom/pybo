from django.urls import path

#from . import views
from .views import base_views,answer_views,question_views,comment_views,vote_views,person_views

#앱을 구분하기 위한 이름.(네임스페이스)
app_name = 'pybo'

urlpatterns=[
    #name은 별칭을 말함.html에서 별칭을 사용할 수 있음.
    #pybo가 생략된 이유는 config/urls.py에 이미 명시되어 있기 때문.
    path('',base_views.index, name='index'),
    #상세조회
    path('<int:question_id>/',base_views.detail, name='detail'),
    #답변등록
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    #답변수정
    path('answer/modify/<int:answer_id>/',answer_views.answer_modify, name='answer_modify'),
    #딥뱐삭제
    path('answer/delete/<int:answer_id>/',answer_views.answer_delete, name='answer_delete'),
    #질문등록
    path('question/create/', question_views.question_create,name='question_create'),
    #질문수정
    path('question/modify/<int:question_id>/',question_views.question_modify, name='question_modify'),
    #질문삭제
    path('question/delete/<int:question_id>/',question_views.question_delete, name='question_delete'),
    #댓글 작성,수정,삭제
    path('comment/create/question/<int:question_id>/', comment_views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question, name='comment_delete_question'),
    path('comment/create/answer/<int:answer_id>/', comment_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', comment_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', comment_views.comment_delete_answer, name='comment_delete_answer'),
    #추천기능
    path('vote/quetion/<int:question_id>/',vote_views.vote_question,name='vote_question'),
    path('vote/answer/<int:answer_id>/',vote_views.vote_answer,name='vote_answer'),

    #특정사용자가 쓴글
    path('person/list/<int:user_id>/',person_views.person_list,name='person_list'),

    #내가 쓴글
    path('list/',person_views.list,name='list'),
    path('detail/<int:question_id>',person_views.person_detail,name='person_detail'),
    path('person/question/modify/<int:question_id>/',person_views.person_question_modify, name='person_question_modify'),
    path('person/question/delete/<int:question_id>/',person_views.person_question_delete, name='person_question_delete'),
    #내가 답변한 글
    path('answer/list/',person_views.my_answer,name='my_answer'),
    path('answer/list/<int:question_id>',base_views.detail,name='my_answer_detail'),
    path('person/answer/modify/<int:answer_id>/',person_views.person_answer_modify, name='person_answer_modify'),
    path('person/answer/delete/<int:answer_id>/',person_views.person_answer_delete, name='person_answer_delete'),
    path('person/comment/create/answer/<int:answer_id>/', person_views.person_comment_create_answer, name='person_comment_create_answer'),
    path('person/comment/modify/answer/<int:comment_id>/', person_views.person_comment_modify_answer, name='person_comment_modify_answer'),
    path('person/comment/delete/answer/<int:comment_id>/', person_views.person_comment_delete_answer, name='person_comment_delete_answer'),
    #내가추천한글
    path('voter/list/',person_views.my_voter,name='my_voter'),


    path('url_test/',person_views.test, name='test'),
]