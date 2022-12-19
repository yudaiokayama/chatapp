from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "myapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:customuser_id>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('changeusername', views.ChangeUsername.as_view(),name='changeusername'),
    path('userchange_done', views.UserChangeDone.as_view(), name='userchange_done'),
    path('changeemail',views.ChangeEmail.as_view(),name='changeemail'),
    path('changeemail_done',views.ChangeEmailDone.as_view(),name='changeemail_done'),
    path('changeicon',views.ChangeIcon.as_view(),name='changeicon'),
    path('changeicon_done',views.ChangeIconDone.as_view(),name='changeicon_done'),
    path('changepwd',views.ChangePwd.as_view(),name='changepwd'),
    path('password_change_done',views.ChangePwdDone.as_view(),name='password_change_done'),
    path('logout', views.Logout.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)