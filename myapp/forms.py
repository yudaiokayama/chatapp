from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Contents
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email','password1','password2','usericon',)
        labels = {'username': 'ユーザー名', 'email': 'メールアドレス', 'password1':'パスワード','password2':'パスワード(確認用)','usericon':'画像',}
    

class LoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for fields in self.fields.values():
            fields.widget.attrs['placeholder']=fields.labels

class ChatContents(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Contents
        fields = ('sender','receiver','message', 'created_at')
        exclude = ['sender','receiver','created_at']
        labels = {'message':''}


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
        ]
        labels = {'username':'新しいユーザー名'}

    def __init__(self, username=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        if username:
            self.fields['username'].widget.attrs['value'] = username

    def update(self, user):
        user.username = self.cleaned_data['username']
        user.save()
        
class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
        ]
        labels = {'email':'新しいメールアドレス'}

    def __init__(self, email=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if email:
            self.fields['email'].widget.attrs['value'] = email

    def update(self, user):
        user.email = self.cleaned_data['email']
        user.save()
        
class IconChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'usericon',
        ]
        labels = {'usericon': '新しいアイコン：'}

    def __init__(self, usericon=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if usericon:
            self.fields['usericon'].widget.attrs['value'] = usericon

    def update(self, user):
        user.usericon = self.cleaned_data['usericon']
        user.save()