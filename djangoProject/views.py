from django.http import HttpResponse
from django.shortcuts import render
# render 'html' file 을 보여줌!


def base_response(request):
    return HttpResponse("안녕하세요! 장고의 시작입니다!")

def first_view(request):
    return render(request, 'my_test.html')
# 'my_test.html'을 보여주는 함수 ---> url과 연동해주어야한다!