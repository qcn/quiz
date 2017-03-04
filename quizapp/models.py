from django.db import models

# Create your models here.

# constants - in practice, pull these into a config file
MAX_TITLE_LENGTH = 50
MAX_QUESTION_LENGTH = 1000
MAX_MC_ANSWER_LENGTH = 500
MAX_SHORT_TEXT_LENGTH = 30


class Quiz(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LENGTH)


class Question(models.Model):
    qz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=MAX_QUESTION_LENGTH)

    class Meta:
        abstract = True # wrapper for an actual question


# multiple choice question
class MCQuestion(Question):

    # if order of answers doesn't matter, we can randomise
    randomise_answers = models.BooleanField(default=False)


# short answer question
class SAQuestion(Question):
    pass


# multiple choice answer
class MCAnswer(models.Model):
    # link to question - if question deleted, delete answer
    qn = models.ForeignKey(MCQuestion, on_delete=models.CASCADE)
    text = models.CharField(max_length=MAX_MC_ANSWER_LENGTH)
    # short text for analysis
    short_text = models.CharField(max_length=MAX_SHORT_TEXT_LENGTH)
    # store correctness here in case future quizzes have multiple
    # correct answers
    correct = models.BooleanField()
