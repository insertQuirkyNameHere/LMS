from django.urls import path
from .views import HomePage, LoginView, MemberRegisterView, UserScramble, PasswordReset

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/member/', MemberRegisterView.as_view(), name='memberRegister'),
    path('resetPassword/', PasswordReset.as_view(), name='passwordReset'),
    path('userScramble/', UserScramble.as_view(), name='userScramble'),
]