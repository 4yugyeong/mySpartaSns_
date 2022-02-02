# tweet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('tweet/', views.tweet, name='tweet'),  # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('tweet/delete/<int:id>', views.delete_tweet, name='delete-tweet'),
    path('tweet/<int:id>', views.detail_tweet, name='detail-tweet'),
    path('tweet/comment/<int:id>', views.write_comment, name='write-comment'),
    path('tweet/comment/delete/<int:id>', views.delete_comment, name='delete-comment'),
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
]

# home 함수는 tweet의 views.py 에 들어가서 유저면 tweet 함수를 실행시켜주고 유저가 아니라면 로그인페이지로 다시 돌아가게 하던지 하는 함수
# tweet 함수는 request가 get으로 요청이 온다면 tweet/home.html 화면을 띄워주는 역할을 한다!
# <int:id> 숫자가 올건데 id 값이 온다! --> delete 함수로 연결