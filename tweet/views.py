from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required
# 로그인한 사람만이 무엇을 할 수 있다!
# tweetmodel을 가져 와서 작업을 한다.


# Create your views here.
def home(request):
    user = request.user.is_authenticated
# home 이라는 함수를 실행 시킴으로서, 유저가 로그인이 되어있는지 인증이 되어있는지 한번에 확인 가능!
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


# tweet 을 보여 주는 함수
def tweet(request):
    if request.method == 'GET':     # 보여지는 것이니까 GET!
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            # "all_twee"t에 변수 저장!
            # 'TweetModel.objects.all()' tweetmodel 안에 저장되어있는 db 모두 불러 올건데 먼저 저장된 순서대로 올라온다!
            # 보통 sns는 최신순 먼저 올라온다 ---> 시간 순서대로 올라 오는 것이 아니라 최신순으로 올라오기 때문이다!
            # '.order_by('-created_at')' 시간을 역순으로 출력해 주려고 '-' 썼다!
            # "all_tweet"을 화면에 넘겨주기만 하면 된다! {'tweet': all_tweet}
            return render(request, 'tweet/home.html', {'tweet': all_tweet})     # 딕셔너리 형태로 tweet 넘겨줌!
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('my-content', '')
        tags = request.POST.get('tag', '').split(',')
        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다.', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=request.user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    my_tweet.tags.add(tag)
            my_tweet.save()
            # my_tweet = TweetModel()
            # my_tweet.author = user
            # my_tweet.content = request.POST.get('my-content', '')
            # my_tweet.save()
            return redirect('/tweet')

# 각각의 함수들을 이어줄 URL을 만들어야 한다.


@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')
# 로그인한 사용자만이 삭제 할 수 있게 이 함수를 실행시킬 권한을 주어야 한다!
# 함수를 만들었으니까 항상 url과 연동을 시켜주어야 한다!
# 특정 인자만 받아와야 하니깐 id!

# detail_tweet(tweet 상세 보기 기능 추가) / write_comment / delete_comment


@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    # 댓글 모델 가져 오기
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    # 최신 순으로 나열 하기 위해서
    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment':tweet_comment})


@login_required
def write_comment(request, id):     # id 값 "detail_tweet"의 id
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/'+str(id))
        # "tweet" 의 id


def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id    # 중간에 있는 이유는 comment.tweet.id 를 하고 나면 지워져 버림!
    comment.delete()
    return redirect('/tweet/'+str(current_tweet))
    # delete를 하고 그 상태로 남아 detail_tweet 페이지에 그대로 머물러 있었음 좋겠다.
    # 여기서 id 값은 "write_comment"의 id

class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

