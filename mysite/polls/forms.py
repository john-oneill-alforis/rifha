from django import forms


class interviewForm(forms.Form):
    subject_uuid = forms.CharField(label="Subject UUID", max_length=36)
    question_1 = forms.CharField(widget=forms.Textarea label="Question 1")
    question_2 = forms.CharField(label="Question 2")
    question_3 = forms.CharField(label="Question 3")
    question_4 = forms.CharField(label="Question 4")
    question_5 = forms.CharField(label="Question 5")
    question_6 = forms.CharField(label="Question 6")
    question_7 = forms.CharField(label="Question 7")
    question_8 = forms.CharField(label="Question 8")
    question_9 = forms.CharField(label="Question 9")
    question_10 = forms.CharField(label="Question 10")
