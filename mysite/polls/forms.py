from django import forms
from .models import interviewee


class interviewForm(forms.Form):
    subject_uuid = forms.CharField(label="Subject UUID", max_length=36)
    question_1 = forms.CharField(widget=forms.Textarea)
    question_2 = forms.CharField(widget=forms.Textarea)
    question_3 = forms.CharField(widget=forms.Textarea)
    question_4 = forms.CharField(widget=forms.Textarea)
    question_5 = forms.CharField(widget=forms.Textarea)
    question_6 = forms.CharField(widget=forms.Textarea)
    question_7 = forms.CharField(widget=forms.Textarea)
    question_8 = forms.CharField(widget=forms.Textarea)
    question_9 = forms.CharField(widget=forms.Textarea)
    question_10 = forms.CharField(widget=forms.Textarea)


class createInterviewee(forms.Form):
    interviewee_reference = forms.CharField(label="Subject UUID", max_length=36)
    interviewee_role = forms.CharField(
        label="Organisational Role", widget=forms.TextInput
    )
    interviewee_fte = forms.CharField(
        label="Organisational FTE", widget=forms.TextInput
    )
    interviewee_org_type = forms.CharField(
        label="Organisation Sector", widget=forms.TextInput
    )


class createResearchQuestion(forms.Form):
    question_text = forms.CharField(label="Question Text", widget=forms.Textarea)


class createResearchResponse(forms.Form):
    interviewee = forms.ChoiceField(
        choices=[
            (obj.interviewee_id, obj.interviewee_reference)
            for obj in interviewee.objects.all()
        ],
        label="Select Interviewee",
    )

    question_1 = forms.CharField(widget=forms.Textarea)
    question_2 = forms.CharField(widget=forms.Textarea)
    question_3 = forms.CharField(widget=forms.Textarea)
    question_4 = forms.CharField(widget=forms.Textarea)
    question_5 = forms.CharField(widget=forms.Textarea)
    question_6 = forms.CharField(widget=forms.Textarea)
    question_7 = forms.CharField(widget=forms.Textarea)
    question_8 = forms.CharField(widget=forms.Textarea)
    question_9 = forms.CharField(widget=forms.Textarea)
    question_10 = forms.CharField(widget=forms.Textarea)
