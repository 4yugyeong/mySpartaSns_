"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from . import views
# 지금 내가 있는 파일에서 views 라는 파일을 가져올거야!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.base_response, name='first_test'),
    path('first/', views.first_view, name='first_view'),
    path('', include('user.urls')),
    # user의 url과 sns의 url 연결!, 그 담에 url에 맞는 view를 작성 해주어야 한다!
    # 유저의 urls를 추가 해주었기 때문에 작동을 유저의 url이 작동을 하는 것이다!
    path('', include('tweet.urls')),
    # 맨 마지막에 , 찍는거 잊지 말기!
]
