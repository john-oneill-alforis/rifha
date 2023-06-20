from django import forms
from .models import (
    assetsClassifications,
    assetsTypes,
    assets,
    staff,
    riskReg,
    threatCatalogue,
    controlCatalogue,
)
from django.forms import DateInput


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


class assetEditForm(forms.ModelForm):
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


class addRiskForm(forms.ModelForm):
    class Meta:
        model = riskReg
        fields = [
            "riskId",
            "riskAsset",
            "riskOwner",
            "riskCreationDate",
            "riskReviewDate",
            "riskNotes",
            "riskDescription",
        ]

        widgets = {
            "riskId": forms.TextInput(attrs={"readonly": "readonly"}),
            "riskCreationDate": DateInput(attrs={"type": "date"}),
            "riskReviewDate": DateInput(attrs={"type": "date"}),
            "riskNotes": forms.Textarea(attrs={"rows": 3, "cols": 30}),
            "riskDescription": forms.Textarea(attrs={"rows": 3, "cols": 30}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """self.fields["assetType"].widget = forms.Select(
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
        )"""
        self.fields["riskAsset"].widget = forms.Select(
            choices=[("", "---------")]
            + list(assets.objects.values_list("assetId", "assetName"))
        )
        self.fields["riskOwner"].widget = forms.Select(
            choices=[("", "---------")]
            + list(staff.objects.values_list("staffId", "fullName"))
        )
        # Retrieve all unique threat categories from the threatCatalogue model
        """threat_categories = threatCatalogue.objects.values_list(
            "threatCategory", flat=True
        ).distinct()

        # Create a choices list organized by threat category
        choices = [("", "---------")]
        for category in threat_categories:
            threats = threatCatalogue.objects.filter(threatCategory=category)
            threat_choices = [
                (threat.threatId, threat.threatName) for threat in threats
            ]
            choices.append((category, threat_choices))

        # Assign the choices to the riskThreats widget
        self.fields["riskThreats"].widget.choices = choices
        self.fields["riskThreats"].widget.attrs["size"] = 10
        self.fields["riskThreats"].required = False"""

        """if self.instance:
            self.fields["riskThreats"].queryset = threatCatalogue.objects.all()
            self.fields["riskThreats"].initial = self.instance.riskThreats.all()
            self.fields["riskThreats"].widget.attrs["size"] = 10"""


class addRiskAnalysisForm(forms.ModelForm):
    class Meta:
        model = riskReg
        fields = [
            "riskId",
            "riskAsset",
            "riskOwner",
            "riskCreationDate",
            "riskReviewDate",
            "riskNotes",
            "riskDescription",
            "riskAnalysisStatus",
            "riskThreats",
        ]

        widgets = {
            "riskId": forms.TextInput(attrs={"readonly": "readonly"}),
            "riskCreationDate": DateInput(attrs={"disabled": "disabled"}),
            "riskReviewDate": DateInput(attrs={"disabled": "disabled"}),
            "riskNotes": forms.Textarea(attrs={"rows": 3, "cols": 30}),
            "riskDescription": forms.Textarea(
                attrs={"rows": 3, "cols": 30, "disabled": "disabled"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["riskAsset"].widget = forms.Select(
            attrs={"disabled": "disabled"},
            choices=[("", "---------")]
            + list(assets.objects.values_list("assetId", "assetName")),
        )
        self.fields["riskOwner"].widget = forms.Select(
            attrs={"disabled": "disabled"},
            choices=[("", "---------")]
            + list(staff.objects.values_list("staffId", "fullName")),
        )
        self.fields["riskThreats"].widget = forms.Select(
            choices=[("", "---------")]
            + list(threatCatalogue.objects.values_list("threatId", "threatName")),
        )


class addRiskThreatForm(forms.ModelForm):
    class Meta:
        model = riskReg
        fields = [
            "riskThreats",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["riskThreats"].widget = forms.Select(
            choices=[("", "---------")]
            + list(threatCatalogue.objects.values_list("threatId", "threatName")),
        )


class addRiskControlForm(forms.ModelForm):
    class Meta:
        model = riskReg
        fields = [
            "riskControls",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["riskControls"].widget = forms.Select(
            choices=[("", "---------")]
            + list(controlCatalogue.objects.values_list("controlId", "controlName")),
        )
