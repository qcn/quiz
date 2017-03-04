from django.shortcuts import render, get_object_or_404
from django.forms import formset_factory
from .forms import MCForm, SAForm, BaseMCFormSet
from .models import Quiz, QuizAnswerSet
from django.http import HttpResponseForbidden

# Create your views here.

'''
def take_quiz(request, **kwargs):
    qz = get_object_or_404(Quiz, pk=kwargs['quizid'])
    MCFormSet = formset_factory(MCForm, formset=BaseMCFormSet)
    formset = MCFormSet()
    return render(request, 'take_quiz.html', {'formset': formset})
'''

def take_quiz(request, **kwargs):
    qz = get_object_or_404(Quiz, pk=kwargs['quizid'])
    # create a form for each question in the quiz
    # oops - this is where the database model breaks down.
    # would have probably been better to have just one generic Question
    # class, and a flag to say which type of question it is, to make
    # this neat. However, I'm here now so let's just go with the MC 
    # questions before the SA questions.
    mcqns = qz.get_mc_questions()
    mc_forms = [MCForm(qn, prefix="mc"+str(qn.pk)) for qn in mcqns]
    saqns = qz.get_sa_questions()
    sa_forms = [SAForm(qn, prefix="sa"+str(qn.pk)) for qn in saqns]
    qn_forms = mc_forms + sa_forms
    return render(request, 'take_quiz.html',
                           {
                            'qn_forms': qn_forms,
                            'qz': qz,
                           })


def submit_quiz(request, **kwargs):
    qz = get_object_or_404(Quiz, pk=kwargs['quizid'])
    # Construct a new QuizAnswerSet from the form data
    if request.method == 'POST':
        # iterate through each of the questions
        # create and assign a dictionary
        answer_dict = {}
        for key in request.POST:
            if key[:2] == "mc": # multiple choice prefix
                # cut off the prefix and suffix
                qn_id = int(key[2:-8])
                answer_dict[qn_id] = [int(x) for x in request.POST[key]]
            elif key[:2] == "sa": # short answer prefix
                # cut off the prefix and suffix
                qn_id = int(key[2:-8])
                answer_dict[qn_id] = request.POST[key]
        # we don't care about anything else like CSRF tokens

        # save new QuizAnswerSet
        new_answers = QuizAnswerSet(qz=qz, answers=answer_dict)
        new_answers.save()

        # redirect to confirmation page
        return render(request, 'quiz_submitted.html',
                        {
                            'qz': qz,
                        })

    # this page should only be accessed by a submission
    return HttpResponseForbidden(
        "You do not have permission to access this page")
