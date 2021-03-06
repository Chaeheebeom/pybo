from django.urls import path, include

from django.contrib.auth import views as auth_views

from . import views
app_name = 'common'

urlpatterns=[
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view() ,name='logout'),
    path('signup/', views.signup ,name='signup'),
    path('find/password/',views.findpassword,name='findpassword'),
    path('profile/',views.profile,name='profile'),
    # 방명록
    path('visitor/', views.visitor, name='visitor'),
    # 코로나 현황
    path('covid/',views.covid, name='covid'),

]