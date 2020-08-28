from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        #html로 부터 전달받은 데이터를 form객체에 저장
        form = QuestionForm(request.POST)
        #전송된 입력값들이 유효한지 검사 만약 유효하지 않다면 form객체에 저장되어 리턴됨.
        if form.is_valid():
            question = form.save(commit=False) #폼을 통해 생성된 객체만 Question모델에다가 리턴해줌
            question.create_date = timezone.now()
            question.author = request.user
            question.save() #db에 저장
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request,'pybo/question_form.html',context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        #넌필드 오류발생시 사용
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail',question_id=question_id)
    #폼객체 생성시 instance를 지정해주면 화면에 모델에 받아온 데이터를 뿌려주게 된다.
    if request.method=='POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date= timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'pybo/question_form.html',context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question= get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request,'삭제권한이 없습니다.')
        return redirect('pybo:detail',question_id=question_id)
    question.delete()
    return redirect('pybo:index')