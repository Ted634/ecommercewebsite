from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


# 建立自定義的使用者創建表單 欄位有:使用者名稱，密碼，確認密碼，勾選學生身分，勾選老師身分
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2',
                  'is_consumer', 'is_seller')
