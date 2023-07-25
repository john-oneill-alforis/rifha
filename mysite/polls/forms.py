from django import forms
from .models import interviewee,researchQuestion,transcriptCapture


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


class createInterviewee(forms.ModelForm):
    class Meta:
        model = interviewee
        fields = ["interviewee_reference",
                    "interviewee_role",
                    "interviewee_fte",
                    "interviewee_org_type"]
        
class createResearchQuestion(forms.Form):
    question_text = forms.CharField(label="Question Text", widget=forms.Textarea)


class createResearchResponse(forms.Form):
    interviewee_choices = [
        (interviewee.interviewee_id, interviewee.interviewee_reference)
        for interviewee in interviewee.objects.all()
    ]

    interviewee = forms.ChoiceField(
        choices=interviewee_choices,
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


class logResearchResponse(forms.ModelForm):
    class Meta:
        model = transcriptCapture
        fields = [
            "interviewee_id",
            "question_id",
            "primary_answer_text",
            "secondary_answer_text",
        ]

        widgets = {
            "primary_answer_text": forms.Textarea(attrs={"rows": 10, "cols": 60}),
            "secondary_answer_text": forms.Textarea(attrs={"rows": 10, "cols": 60}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["interviewee_id"].widget = forms.Select(
            #attrs={"disabled": "disabled"},
            choices=[("", "---------")]
            + list(interviewee.objects.values_list("interviewee_id", "interviewee_reference")),
        )
        self.fields["question_id"].widget = forms.Select(
            #attrs={"disabled": "disabled"},
            choices=[("", "---------")]
            + list(researchQuestion.objects.values_list("question_id", "question_text")),
        )

       
