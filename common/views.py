from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render,redirect
from common.forms import UserForm,FindPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .commonUtils import getTempPassword,send_email

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
