from django import forms
from .models import assetsClassifications, assetsTypes, assets, staff


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


class classificationAddForm(forms.Form):
    classificationLabel = forms.CharField(
        widget=forms.TextInput, label="Classification Label"
    )
    classificationDescription = forms.CharField(
        widget=forms.Textarea, label="Classification Description"
    )


class classificationEditForm(forms.ModelForm):
    class Meta:
        model = assetsClassifications
        fields = ["classificationLabel", "classificationDescription"]
        widgets = {
            "classificationLabel": forms.TextInput(),
            "classificationDescription": forms.Textarea,
        }


class assettTypeAddForm(forms.Form):
    assetTypeLabel = forms.CharField(widget=forms.TextInput, label="Asset Type Label")
    assettTypeDescription = forms.CharField(
        widget=forms.Textarea, label="Asset Type Description"
    )


class assetTypesEditForm(forms.ModelForm):
    class Meta:
        model = assetsTypes
        fields = ["assetTypeName", "assetTypeDescription"]
        widgets = {
            "assetTypeName": forms.TextInput(),
            "assetTypeDescription": forms.Textarea,
        }


class addAssetForm(forms.ModelForm):
    assetType = forms.ModelChoiceField(
        queryset=assetsTypes.objects.all(), label="Asset Type"
    )

    assetClassificaion = forms.ModelChoiceField(
        queryset=assetsClassifications.objects.all(), label="Asset Classification"
    )

    class Meta:
        model = assets
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assetType"].widget = forms.Select(
            choices=assetsTypes.objects.values_list("assetTypeId", "assetTypeName")
        )
        self.fields["assetClassification"].widget = forms.Select(
            choices=assetsClassifications.objects.values_list(
                "classification_Id", "classificationLabel"
            )
        )
        self.fields["assetOwner"].widget = forms.Select(
            choices=staff.objects.values_list("staffId", "jobTitle")
        )
