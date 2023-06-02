from django import forms


class interviewForm(forms.Form):
    subject_uuid = (forms.CharField(label="Subject UUID", max_length=36),)
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
