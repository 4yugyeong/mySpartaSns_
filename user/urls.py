from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    path('user_follow/', views.user_follow, name='user-follow')
    # 버튼을 추가하여서 logout url 이 작동 시켜줄 수 있도록 할 것이다! --> templates base.html (사이트의 상단 nav bar에 로그아웃 기능을 추가 하고 싶기 때문이다!
]
