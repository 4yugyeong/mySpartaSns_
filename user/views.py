from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model  # 사용자가 데이터데베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# 화면에 글자를 나타내 주는 것으로 HttpResponse 썻었다!
# 'HttpResponse' 를 통해 로그인이 성공하였다면 성공하였다는 msg를 출력하고, 로그인이 실패를 하였다면, 실패 msg를 출력한다!
# 이어 주는 url 그 담에 보여 주는 view 함수 수정
# 세션 사용자 정보를 저장 하는 공간
# '.' 나의 위치와 동일한 친구 중에 models을 갖고 올 건데 그 models 중에서 'UserModel'이라는 친구를 가지고 오겠다!
# render를 통해서 화면에 보여주는 html을 보여주는 역할을 한다!
# Create your views here.
# 화면에서 장고 서버로 url 요청 ---> 어떤 url로 요청 ---> 장고에서 이 url이 왔네? ---> 이 url의 요청방식은 어떤 거지 하고 먼저 보게 된다!
# 그때 if문 실행! ---> 화면


def sign_up_view(request):
    if request.method == 'GET':  # GET 메서드로 요청이 들어 올 경우
        user = request.user.is_authenticated
        if user:
            return redirect('/')    # '/' tweetapp에 home!
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        # POST 메서드로 요청이 들어 올 경우
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            # 패스워드가 같지 않다고 알람
            return render(request, 'user/signup.html', {'error': '패스워드를 확인 해 주세요!'})
        # 'password'와 'password2'가 같지 않다면, 저장이 되면 안된다!
        # 다시 해당하는 화면을 보여주려고 한다! GET에서 사용했던 화면을 다시 보여 줄 거다!
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밀번호는 필수 값 입니다.'})
            exist_user = get_user_model().objects.filter(username=username)
            # exist_user = UserModel.objects.filter(username=username)
            # UserModel에서 user model을 갖고 올거다! 어떤 조건으로 어떤 filter로 갖고 올건데? username이 내가 입력한 username인 사용자가 있는지 검색
            # '.filter()'함수는 데이터가 있으나 없으나 에러를 발생 하지 않는다.
            # 데이터가 있으면 검색해서 가져오고 없으면 없음으로 표현해준다!
            if exist_user:
                return render(request, 'user/signup.html', {'error': '사용자가 존재합니다.'})
                # user가 없다면, 나는 그 사용자가 회원가입을 해도 된다고 생각하기 때문에, db에 저장 해줄거다!
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                # 사용자 저장 하는 기능!
                # new_user = UserModel()
                # 클래스 예제와 똑같다!
                # new_user.username = username
                # new_user.password = password
                # new_user.bio = bio
                # new_user.save()
                # 저장한 담에는 redirect를 통해서 회원가입 페이지를 만들어 주고 싶다! 위에 render 옆에 redirect 함수 추가!
            return redirect('/sign-in')
            # 회원가입 완료 되었을 때만 실행!
            # 'new_user.username'이라는 변수에다가 username을 저장해준다!
            # 만약 'password'와 'password2'가 같다면, 더이상 나쁜 일이 없다!
            # 'new_user'라는 변수에다가 UserModel 클래스를 가져올거다!
            # POST로 가져온 data를 이렇게 받고요! 'request.POST.get' 로 가져온 데이터가 많이 있는데 그 중에서 나는 'username' 으로만 되어있는 data만 받겠다!
            # 만약 'username'으로만 되어 있는 것이 없다면, 'None'으로 빈칸으로 처리하겠다!
            # 그리고 그 가져온 정보를 'username'이라는 변수에 저장한다!
            # 어떤 작업이 들어갈지 모르니까!(db 데이터 저장하는 기능)

            # signup과 singin 파일을 연결 시켜 준다!
            # singup, signin 함수를 만들어 주었다!
            # 'return render' 화면을 보여준다!
            # 어떤 화면? 'user/signup.html' 화면


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)   # 인증
        # 인증 기능 모듈을 먼저 불러 온다.
        # 암호화 된 pw와 유저가 입력 하는 pw가 같은지 아닌지 확인 해주고, 모든 로그인 정보를 들고와 준다.
        # me = UserModel.objects.get(username=username)
        # 로그인 'object.get()'이라는 친구는 데이터가 무조건 있어야 한다. 데이터가 사용자가 없다면 에러가 난다.
        if me is not None:  # 사용자가 비어있지 않다!
            auth.login(request, me)     # 내 정보를 넣어준다!
            return redirect('/')
            # 로그인을 한 다음에 바로 home으로 들어가게끔 만들어 준다!
            # return HttpResponse(me.username)
        else:
            return render(request, 'user/signin.html', {'error': '유저이름 또는 패스워드를 확인 해 주세요.'})
        # 기존에 유저가 있는지 먼저 한번 확인
        # 'usermodel'은 이미 데이터베이스와 연결이 되어있는 객체(클래스) 거기에서 우리가 어떤 데이터를 가지고 올건지 우리가 조건을 써주어야 한다!
        # 빨간색 'username'은 우리가 넣어준 username이 아니라 'UserModel' 안에 있던 username! db안에서 우리 POST에서 받아온 데이터와 같은 친구를 불러오는 거다!
        # 'me' 를 통과 하기 위해서는 db안에 저 username을 적은 사용자가 있어야 한다!
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')
        # 로그인이 되어 있는 사용자가 있는지 없는지 판별해주는 조건문을 곳곳에 페이지를 보여줄 때 마다 넣어서 지금처럼 잘 작동하게 만들었다!
        # views.py를 만들어 주었으니깐 url과 연동을 시켜주어야 한다!


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
# 유저가 있다면 tweet 페이지로 이동시켜 줄거고, 없다면 회원가입 페이지로 이동시켜 준다!
# 로그아웃 기능구현을 하였으니, urls.py에다가 로그아웃 기능 추가 해주어야 한다.
# @login_required 사용자가 꼭 로그인이 되어있어야지만, 접근이 가능한 함수이다!


# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})
    # exclude 해당 하는 data 에서 어떤 것을 빼겠다
    # 내가 나를 팔로우 할 수 없고 볼 수도 없게 만든다


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    # click_user --> 내가 방금 누른 사람!
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    # me 로그인 한 사용자, click_user 내가 팔로우 하려고 하거나, 팔로우 취소를 할 사용자 그 사람의 모델을 가져와서 그 사용자의 팔로우 하는 사람 전부를 가져온다!
    # 팔로우 하는 사람 모든 사람 중에서 내가 있다면, 그 안에서 제거
    # 만약 그 사용자 모델 안에 내가 있다면 이미 팔로우를 하고 있기 때문에 다시 한번 팔로우를 눌렀을 경우, 팔로우를 취소 해주면 된다!
    else:
        click_user.followee.add(request.user)
        # 만약 그 사람이 없다면 팔로우를 에드 해주면 된다
        # 그 전부 중에 내가 팔로우 하고 있지 않다면, 팔로우 하게 해준다
    return redirect('/user')
    # view에 입력을 했으면 url과 연결!