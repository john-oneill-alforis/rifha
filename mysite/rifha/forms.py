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


class assetEditForm(forms.Form):
    assetName = forms.CharField(widget=forms.TextInput, label="Asset Type Label")
    assetDescription = forms.CharField(
        widget=forms.Textarea, label="Asset Type Description"
    )

    assetType = forms.ModelChoiceField(
        queryset=assetsTypes.objects.values_list("assetTypeName"),
        label="Asset Type",
    )

    assetClassification = forms.ModelChoiceField(
        queryset=assetsClassifications.objects.all(),
        label="Asset Classification",
    )

    assetOwner = forms.ModelChoiceField(
        queryset=staff.objects.all(),
        label="Asset Owner",
    )


class addAssetForm(forms.ModelForm):
    class Meta:
        model = assets
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assetType"].widget = forms.Select(
            choices=[("", "---------")]
            + list(assetsTypes.objects.values_list("assetTypeId", "assetTypeName"))
        )
        self.fields["assetClassification"].widget = forms.Select(
            choices=[("", "---------")]
            + list(
                assetsClassifications.objects.values_list(
                    "classification_Id", "classificationLabel"
                )
            )
        )
        self.fields["assetOwner"].widget = forms.Select(
            choices=[("", "---------")]
            + list(staff.objects.values_list("staffId", "fullName"))
        )
