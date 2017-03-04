from django import forms
from .models import Quiz, MCQuestion, MCAnswer, SAQuestion


class MCForm(forms.Form):
    def __init__(self, qn, *args, **kwargs):
        super(MCForm, self).__init__(*args, **kwargs)
        # get the list of possible answers, convert to text
        choices = [str(x) for x in qn.get_answers()]

        # find out what kind of widget/field to use
        # this assumes that if a question only has one answer,
        # we only want the student to select one answer -
        # alternatively every question could be rendered with checkboxes
        if qn.has_multiple_answers():
            self.fields['answers'] = forms.MultipleChoiceField(
                                        choices=choices,
                                        widget=CheckboxSelectMultiple)
        else:
            self.fields['answers'] = forms.ChoiceField(
                                        choices=choices,
                                        widget=RadioSelect)

        # we'd probably validate the not sure mutual exclusion case
        # within this form if we were going to do that


class SAForm(forms.Form):
    def __init__(self, qn, *args, **kwargs):
        super(SAForm, self).__init__(*args, **kwargs)
        self.fields['answers'] = forms.TextField()
