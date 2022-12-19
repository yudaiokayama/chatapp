from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView
from .forms import CustomUserCreationForm, LoginForm, ChatContents ,UserChangeForm, EmailChangeForm, IconChangeForm
from .models import CustomUser, Contents
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.views.generic.base import TemplateView


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    form = CustomUserCreationForm()
    if request.POST:
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
           form.save()
           return redirect('/')
    else:
        return render(request, "myapp/signup.html", {'form':form,})
 

class Login(LoginView):
    template_name = "myapp/login.html"
    form = LoginForm


@login_required
def friends(request):
    new_friends_list = CustomUser.objects.filter(
        ~Q(username=request.user)).all()
    
    user = request.user
    
    info = []
    info_have_message = []
    info_have_no_message = []

    for friend in new_friends_list:
        latest_message = Contents.objects.filter(
            Q(sender=user,receiver=friend) | Q(receiver=user,sender=friend)
        ).order_by('created_at').last()
        if latest_message:
            info_have_message.append([friend, latest_message.message, latest_message.created_at]) ###info_have_messageではなくinfoにしたら動く
        else:
            info_have_no_message.append([friend, None, None]) 
    
    info.extend(info_have_message)
    info.extend(info_have_no_message)
    context = {
        # 'new_friends_list': new_friends_list,
        'info': info,
        # 'user': user
    }
    return render(request, "myapp/friends.html", context)

@login_required
def talk_room(request, customuser_id):
    friend = get_object_or_404(CustomUser, pk=customuser_id)
    form = ChatContents()
    if request.POST:
        form = ChatContents(request.POST)
        contents = form.save(commit=False)
        contents.sender = request.user 
        contents.receiver = CustomUser.objects.get(id = customuser_id)
        form.save()
    else: 
        form = ChatContents()
    
    contents_sender = request.user
    contents_receiver = CustomUser.objects.get(id = customuser_id)
    message_list = Contents.objects.filter(
        Q(sender__contains=contents_sender, receiver=contents_receiver)|
        Q(sender__contains=contents_receiver, receiver=contents_sender)
    ).all()
   
    context = {
        "friend": friend,
        "form": form,
        "message_list" : message_list,
    }
    return render(request, "myapp/talk_room.html", context)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")


class ChangeUsername(LoginRequiredMixin, FormView):
    template_name = 'myapp/changeusername.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('myapp:userchange_done')
    
    def form_valid(self, form):
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'username' : self.request.user.username,
        })
        return kwargs
 
class UserChangeDone(TemplateView):
    template_name = "myapp/userchange_done.html"
    
class ChangeEmail(LoginRequiredMixin, FormView):
    template_name = 'myapp/changeemail.html'
    form_class = EmailChangeForm
    success_url = reverse_lazy('myapp:changeemail_done')
    
    def form_valid(self, form):
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'email' : self.request.user.email,
        })
        return kwargs
    
class ChangeEmailDone(TemplateView):
    template_name = "myapp/changeemaildone.html"
    
class ChangeIcon(LoginRequiredMixin, FormView):
    template_name = 'myapp/iconchange.html'
    form_class = IconChangeForm
    success_url = reverse_lazy('myapp:changeicon_done')
    
    def form_valid(self, form):
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'usericon' : self.request.user.usericon,
        })
        return kwargs

class ChangeIconDone(TemplateView):
    template_name = "myapp/iconchangedone.html"

class ChangePwd(LoginRequiredMixin,PasswordChangeView):
    template_name = "myapp/changepwd.html"
    success_url = reverse_lazy('myapp:password_change_done')

class ChangePwdDone(LoginRequiredMixin,PasswordChangeDoneView):
    template_name = "myapp/changepwddone.html"

class Logout(LogoutView):
    template_name  = "myapp/index.html"