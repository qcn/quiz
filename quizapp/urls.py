from django.conf.urls import url
from .views import *

app_name = "quizapp"
urlpatterns = [
    url(r'^take/(?P<quizid>[0-9]+)$', take_quiz, name="take"),
    url(r'^take/(?P<quizid>[0-9]+)/submit/$', submit_quiz, name="submit"),
    url(r'^results/(?P<quizid>[0-9]+)/$', view_analysis, name="results"),
]
