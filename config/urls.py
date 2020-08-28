"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from pybo.views import base_views

urlpatterns = [
    #/으로 접속시 pybo의 index로 연결되도록
    path('',base_views.index, name='index'),
    path('admin/', admin.site.urls),
    #pybo url을 호출하면 views.py의 index라는 함수를 호출
    #항상 끝에 정규화를 위해 / 를 붙여주자
    #path('pybo/', views.index),
    #pybo url이 요청되면 pybov폴더의 urls.py의 매핑정보를 읽으라는 뜻.
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')), #로그인/아웃을 위한 url추가

]
