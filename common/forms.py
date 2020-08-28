from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#UserCreationForm의 속성 username,password1, password2
#is_valid()함수 호출시 위 3개를 체크함.
class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일')

    class Meta:
        model = User
        fields = ('username','email')

class FindPasswordForm(forms.ModelForm):

    class Meta:
        model = User
        #속성설정.
        fields =['username','email']

        labels={
            'username':'아이디',
            'email':'이메일',
        }