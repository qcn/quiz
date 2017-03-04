from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^take/(?P<quizid>[0-9]+)$', take_quiz, name="quizapp-take"),
]
