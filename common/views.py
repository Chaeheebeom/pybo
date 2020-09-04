from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render,redirect
from common.forms import UserForm,FindPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .commonUtils import getTempPassword,send_email

import requests
import time
from urllib.parse import unquote
import xml.etree.ElementTree as el


@login_required(login_url='common:login')
def profile(request):
    return render(request, 'common/profile.html')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    context={'form':form}
    return render(request, 'common/signup.html', context)


def findpassword(request):

    if request.method == 'POST':
        form = FindPasswordForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')

        if User.objects.filter(email=email).filter(username=username).exists():
            #맞는 정보를 찾음
            #임시비밀번호로 변경.
            temppassword=getTempPassword()
            u = User.objects.get(username=username)
            u.set_password(temppassword)
            u.save()
            send_email(email,'메일주소변경안내',temppassword)
        else:
            #못찾음
            messages.error(request, '아이디와 이메일을 다시 입력해주세요.')
            return redirect('common:findpassword')
    else:
        form = FindPasswordForm()
    context={"form":form}
    return render(request, 'common/findpassword.html', context)

def visitor(request):

    return render(request,'common/visitor.html')



def covid(request):

    serviceUrl = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
    serviceKey = 'XhXhzNW%2BV19VmW1IWKHPOt5mBgvHbcSxIHHtZcWKjFZwR5PPIAk%2Fn%2FqAyS9hybxU2TPYPmka6MQYYDdReAMmJw%3D%3D'
    serviceKey_decode = unquote(serviceKey)

    pageNo = '2'
    numOfRows = '10'
    startCreateDt = '20200901'
    endCreateDt = time.strftime('%Y%m%d', time.localtime(time.time()))

    parameters = {"serviceKey": serviceKey_decode, "pageNo": pageNo, "numOfRows": numOfRows,
                  "startCreateDt": startCreateDt, "endCreateDt": endCreateDt}

    response = requests.get(serviceUrl, params=parameters)

    print(response.text)

    covidList=[]

    if response.status_code == 200:
        # print("응닫결과 : ",response.text)
        tree = el.fromstring(response.text)
        iter = tree.iter(tag="item")

        for element in iter:

            createDt = element.find('createDt')  # 일시
            deathCnt = element.find('deathCnt')  # 사망자
            area = element.find('gubun')  # 지역
            inDec = element.find('incDec')  # 전일대비증감수
            defCnt = element.find('defCnt')  # 확진자수
            isolClearCnt = element.find('isolClearCnt')  # 격리해제수
            isolIngCnt = element.find('isolIngCnt')  # 격리중환자수
            localOccCnt = element.find('localOccCnt')  # 지역발생수
            overFlowCnt = element.find('overFlowCnt')  # 해외유입수
            qurRate = element.find('qurRate')  # 10만명당 발생률
            id = element.find('seq')  # 게시글번호(고유값)
            stdDay = element.find('stdDay')  # 기준일시
            updateDt  = element.find('updateDt ')  # 수정일시
            data = {"createDt":createDt.text,"deathCnt":deathCnt.text,"area":area.text,"inDec":inDec.text,"isolClearCnt":isolClearCnt.text
                ,"isolIngCnt":isolIngCnt.text,"localOccCnt":localOccCnt.text,"overFlowCnt":overFlowCnt.text,"qurRate":qurRate.text,
                "id":id.text,"stdDay":stdDay.text,"defCnt":defCnt.text}
            covidList.append(data)

    context = {'covidList': covidList}
    print(covidList)
    return render(request,'common/covid.html',context)
