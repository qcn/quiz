from django.db import models
from django import forms

# Create your models here.

# constants - in practice, pull these into a config file
MAX_TITLE_LENGTH = 50
MAX_QUESTION_LENGTH = 1000
MAX_MC_ANSWER_LENGTH = 500
MAX_SHORT_TEXT_LENGTH = 30


VALIDATE_MC_TEXT = "Multiple choice question requires a correct answer"


class Quiz(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    
    def __str__(self):
        return self.title


class Question(models.Model):
    qz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=MAX_QUESTION_LENGTH)

    class Meta:
        abstract = True # wrapper for an actual question
        # assume questions are added in order
        ordering = ['id']

    def __str__(self):
        return self.text


# multiple choice question
class MCQuestion(Question):

    # if order of answers doesn't matter, we can randomise
    randomise_answers = models.BooleanField(default=False)

    # get answers either in order or in random order
    def get_answers(self):
        if (self.randomise_answers):
            return self.mcanswer_set.order_by('?')
        return self.mcanswer_set.all()

    # make sure a multiple choice question has at least one correct answer
    def clean(self):
        super(MCQuestion, self).clean()
        if not self.mcanswer_set.filter(correct=True):
            raise forms.ValidationError(VALIDATE_MC_TEXT)
        

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
    # store correctness here in case questions have multiple
    # correct answers
    correct = models.BooleanField()

    class Meta:
        # for now, assume answers are added in order. Add an ordering
        # field if this isn't the case.
        ordering = ['id']

    def __str__(self):
        return self.text

