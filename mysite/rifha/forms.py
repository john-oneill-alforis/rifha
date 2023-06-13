from django import forms
from .models import staff


class peopleAddForm(forms.Form):
    firstName = forms.CharField(widget=forms.TextInput)
    lastName = forms.CharField(widget=forms.TextInput)
    lastName = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField()
    jobTitle = forms.CharField(widget=forms.TextInput)
    contactNumber = forms.CharField(widget=forms.TextInput)


class peopleEditForm(forms.ModelForm):
    class Meta:
        model = staff
        fields = ["firstName", "lastName", "email", "jobTitle", "contactNumber"]
        widgets = {
            "firstName": forms.TextInput(),
            "lastName": forms.TextInput(),
            "email": forms.EmailInput(),
            "jobTitle": forms.TextInput(),
            "contactNumber": forms.TextInput(),
        }
