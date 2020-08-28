from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from django.db.models import Q,Count

from ..models import Question

def index(request):
    #Get으로 페이지 가져옴 디폴트값은 1
    page = request.GET.get('page','1')
    #검색어 가져옴
    kw = request.GET.get('kw','')
    #정렬기준 가져옴
    so = request.GET.get('so','recent')


    #생성날짜 순으로 정렬해서 모델에서 가져옴
    question_list = Question.objects.order_by('-create_date')

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    #들어온 검색어로 검색.
    if kw:
        #제목, 내용 , 글쓴이, 답변이
        #filter함수에서는 모델속서에 접근하기위해 언더바두개씀
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw)  |
            Q(answer__author__username__icontains=kw)
        ).distinct() #

    #페이지처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj,'page':page,'kw':kw,'so':so}
    #데이터를 템플릿에 적용하여 HTML로 변환
    return render(request, 'pybo/question_list.html', context)

def detail(request,question_id):
    #1개만 가져옴 실패시 에러발생(all()의 경우 빈 쿼리셋 객체를 반환)
    #question = Question.objects.get(id=question_id)
    #못가져올시 404에러 발생
    question = get_object_or_404(Question, pk=question_id)

    answers=question.answer_set.order_by('-create_date').all()

    # Get으로 페이지 가져옴 디폴트값은 1
    page = request.GET.get('page', '1')

    paginator = Paginator(answers, 5)
    page_obj = paginator.get_page(page)

    context = {'question':question,'answer_list':page_obj}
    return render(request,'pybo/question_detail.html', context)