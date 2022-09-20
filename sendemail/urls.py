from django.urls import path
from sendemail.views import *

urlpatterns = [
    path('Email_sending', Email_sending.as_view()),
    path('accounts', accounts.as_view()),
    path('verifycode', verifycode.as_view()),
    path('changepassword', changepassword.as_view()),
    path('login', login.as_view()),


]