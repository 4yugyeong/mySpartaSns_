#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class UserModel(AbstractUser):
# 우리는 장고에서 제공해 주는 기본적인 유저 모델을 사용하겠다!
# 'Abstractuser'는 'auth_user'와 연동되는 클래스!
# 장고 모델에서 주는 걸 우리는 사용할 건데 거기서 추가할 것이 있다!
# 우리가 auth_model에서 지원하지 않는 'bio'만을 남겨 두고 지워줄려 한다!
# 우리가 기본적으로 장고에서 제공해 주는 것을 쓰되, bio라는 것만 추가해서 사용하겠다!
# 우리가 이렇게 수정 한 걸 장고한테 알려 줘야 되는데 usermodel을 수정하는 방법은 조금 다르다!

    class Meta:
        db_table = "my_user"

    # username = models.CharField(max_length=20, null=False)
    # password = models.CharField(max_length=256, null=False)
    bio = models.CharField(max_length=256, default='')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
    # AUTH_USER_MODEL ---> 우리 유저 모델
