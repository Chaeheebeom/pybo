from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect,resolve_url
from django.utils import timezone


from ..forms import QuestionForm, AnswerForm, CommentForm
from django.contrib.auth.models import User
from ..models import Question, Answer, Comment

import json

@login_required(login_url='common:login')
def list(request):

    page = request.GET.get('page','1')

    question = Question.objects.filter(author=request.user).order_by('-create_date')

    paginator = Paginator(question,10)
    page_obj = paginator.get_page(page)

    context = {"question_list" : page_obj,'page':page}
    return render(request, 'person/list.html',context)

@login_required(login_url='common:login')
def my_answer(request):
    page = request.GET.get('page', '1')

    answer=Answer.objects.filter(author=request.user).order_by('-create_date')

    length = len(answer)

    paginator = Paginator(answer, 10)
    page_obj = paginator.get_page(page)

    context = {"answer_list": page_obj, 'page': page,'total':length}
    return render(request, 'person/my_answer_list.html', context)


@login_required(login_url='common:login')
def my_voter(request):
    page = request.GET.get('page', '1')

    question = Question.objects.filter(voter=request.user).order_by('-create_date')


    paginator = Paginator(question, 10)
    page_obj = paginator.get_page(page)

    context = {"voter_list": page_obj, 'page': page}
    return render(request, 'person/my_voter_list.html', context)


def person_list(request,user_id):
    page = request.GET.get('page', '1')

    question = Question.objects.filter(author=user_id).order_by('-create_date')

    paginator = Paginator(question, 10)
    page_obj = paginator.get_page(page)

    context = {"question_list": page_obj, 'page': page}
    return render(request, 'person/list.html', context)

@login_required(login_url='common:login')
def person_detail(request,question_id):
    # 1개만 가져옴 실패시 에러발생(all()의 경우 빈 쿼리셋 객체를 반환)
    # question = Question.objects.get(id=question_id)
    # 못가져올시 404에러 발생
    question = get_object_or_404(Question, pk=question_id)

    answers = question.answer_set.order_by('-create_date').all()

    # Get으로 페이지 가져옴 디폴트값은 1
    page = request.GET.get('page', '1')

    paginator = Paginator(answers, 5)
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list': page_obj}
    return render(request, 'person/detail.html', context)


@login_required(login_url='common:login')
def person_question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    #폼객체 생성시 instance를 지정해주면 화면에 모델에 받아온 데이터를 뿌려주게 된다.
    if request.method=='POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date= timezone.now()
            question.save()
            return redirect('pybo:person_detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'pybo/question_form.html',context)

@login_required(login_url='common:login')
def person_question_delete(request, question_id):
    question= get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('pybo:list')

@login_required(login_url='common:login')
def person_answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    #폼객체 생성시 instance를 지정해주면 화면에 모델에 받아온 데이터를 뿌려주게 된다.
    if request.method=='POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date= timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:my_answer'), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'form':form}
    return render(request, 'pybo/answer_form.html',context)

@login_required(login_url='common:login')
def person_answer_delete(request, answer_id):
    answer= get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    return redirect('pybo:my_answer')

@login_required(login_url='common:login')
def person_comment_create_answer(request, answer_id):

    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:my_answer'), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def person_comment_modify_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:my_answer'), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def person_comment_delete_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('pybo:my_answer')

@login_required(login_url='common:login')
def test(request):
    question_id= request.POST.get('question_id')
    print('pk',question_id)
    q=get_object_or_404(Question,pk=question_id)

    context={ 'id': q.id,'subject':q.subject,'content':q.content,'create_date':str(q.create_date),'modify_date':str(q.modify_date),'author':q.author_id }

    return HttpResponse(json.dumps(context), content_type='application/json')

