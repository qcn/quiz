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
    mc_qns = qz.get_mc_questions()
    mc_forms = [MCForm(qn, prefix="mc"+str(qn.pk)) for qn in mc_qns]
    sa_qns = qz.get_sa_questions()
    sa_forms = [SAForm(qn, prefix="sa"+str(qn.pk)) for qn in sa_qns]
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
                # cut off the suffix - we have to keep the prefix for
                # clashes between MC and SA
                qn_id = key[:-8]
                answer_dict[qn_id] = [int(x) for x in request.POST.getlist(key)]
            elif key[:2] == "sa": # short answer prefix
                # cut off the suffix
                qn_id = key[:-8]
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


def view_analysis(request, **kwargs):
    qz = get_object_or_404(Quiz, pk=kwargs['quizid'])
    # Get questions from the quiz
    mc_qns = qz.get_mc_questions()
    sa_qns = qz.get_sa_questions()
    # Load all the answersets
    answersets = [aset.answers for aset in qz.get_answersets()]

    # Aggregate the results for each MC question

    mc_answers = {}

    for qn in mc_qns:
        poss_answers = qn.get_answers()
        # dictionary showing how many of each response was given
        this_qn = dict.fromkeys([ans.id for ans in poss_answers], 0)
        for aset in answersets:
            # each question has a list of submitted answers
            for answer in aset["mc" + str(qn.id)]:
                this_qn[answer] += 1
        mc_answers[qn.id] = this_qn

    # Concatenate all the short answer responses

    sa_answers = {}

    for qn in sa_qns:
        this_qn = [aset["sa" + str(qn.id)] for aset in answersets]
        sa_answers[qn.id] = this_qn

    # regroup short answer responses for template
    sa_to_template = [{'qn_id': qn.id, 'text': qn.text,
                       'answers': sa_answers[qn.id]} for qn in sa_qns]

    # Do cool things with pie charts and word clouds

    return render(request, 'view_analysis.html',
                    {
                        'qz': qz,
                        'responses': len(answersets),
                        'mc_qns': mc_qns,
                        'mc_answers': mc_answers,
                        'sa_qns': sa_to_template,
                    })
