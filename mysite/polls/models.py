from django.db import models
import uuid
import datetime

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class textLabels(models.Model):
    entryId = models.BigAutoField(primary_key=True)
    label = models.TextField(max_length=200)
    modelAssociated = models.BooleanField()

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label


class trainingCorpus(models.Model):
    entryId = models.BigAutoField(primary_key=True)
    source = models.CharField(max_length=200)
    author = models.CharField(max_length=45)
    publishedDate = models.DateField()
    dateAdded = models.DateField()
    link = models.TextField()
    text = models.TextField()
    linkHash = models.CharField(max_length=256, db_index=True, unique=True)
    included = models.IntegerField(default=1)
    verisCompatible = models.CharField(max_length=45, blank=True, null=True)
    textLabel = models.ForeignKey(
        textLabels,
        on_delete=models.CASCADE,
        default=1,
    )

    def __unicode__(self):
        return self.link

    def __str__(self):
        return self.link


class veris_incident_details(models.Model):
    incident_id = models.CharField(max_length=45, primary_key=True)
    security_incident = models.CharField(max_length=45)
    source_id = models.CharField(max_length=45)

    summary = models.TextField
    analysis_status = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=False, auto_now_add=False)

    master_id = models.CharField(max_length=45)
    modified = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __unicode__(self):
        return self.incident_id


######################################################################
# Veris Incident Information Tables
######################################################################


class veris_incident_details(models.Model):
    incident_id = models.CharField(max_length=45, primary_key=True)
    security_incident = models.CharField(max_length=45)
    source_id = models.CharField(max_length=45)

    summary = models.TextField(default="None")
    analysis_status = models.CharField(max_length=200)
    created = models.DateField(auto_now=False)

    master_id = models.CharField(max_length=45)
    modified = models.DateField(auto_now=False, auto_now_add=False)

    def __unicode__(self):
        return self.name


######################################################################
# Veris Incident Action Information Tables - Malware
######################################################################


class veris_incident_action_details(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    action = models.CharField(max_length=45)

    def __unicode__(self):
        return self.name


class veris_action_malware(models.Model):
    vam_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    cve = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    notes = models.CharField(max_length=1000, null=True)


class veris_action_malware_variety(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vam_Id = models.ForeignKey(
        veris_action_malware,
        on_delete=models.CASCADE,
        default=1,
    )
    variety = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class veris_action_malware_vector(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vam_Id = models.ForeignKey(
        veris_action_malware,
        on_delete=models.CASCADE,
        default=1,
    )
    vector = models.CharField(max_length=200)


class veris_action_malware_notes(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vam_Id = models.ForeignKey(
        veris_action_malware,
        on_delete=models.CASCADE,
        default=1,
    )
    notes = models.CharField(max_length=1000)


class veris_action_malware_results(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vam_Id = models.ForeignKey(
        veris_action_malware,
        on_delete=models.CASCADE,
        default=1,
    )
    result = models.CharField(max_length=200)


######################################################################
# Veris Incident Action Information Tables - Hacking
######################################################################


class veris_action_hacking(models.Model):
    vah_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    cve = models.CharField(max_length=200)
    notes = models.CharField(max_length=1000, null=True)


class veris_action_hacking_variety(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vah_Id = models.ForeignKey(
        veris_action_hacking,
        on_delete=models.CASCADE,
        default=1,
    )
    variety = models.CharField(max_length=200)


class veris_action_hacking_vector(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vah_Id = models.ForeignKey(
        veris_action_hacking,
        on_delete=models.CASCADE,
        default=1,
    )
    vector = models.CharField(max_length=200)


class veris_action_hacking_results(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vah_Id = models.ForeignKey(
        veris_action_hacking,
        on_delete=models.CASCADE,
        default=1,
    )
    results = models.CharField(max_length=1000)


######################################################################
# Veris Incident Action Information Tables - Social
######################################################################


class veris_action_social(models.Model):
    vas_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    notes = models.CharField(max_length=1000, null=True)


class veris_action_social_variety(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vas_Id = models.ForeignKey(
        veris_action_social,
        on_delete=models.CASCADE,
        default=1,
    )
    variety = models.CharField(max_length=200)


class veris_action_social_vector(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vas_Id = models.ForeignKey(
        veris_action_social,
        on_delete=models.CASCADE,
        default=1,
    )
    vector = models.CharField(max_length=200)


class veris_action_social_results(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vas_Id = models.ForeignKey(
        veris_action_social,
        on_delete=models.CASCADE,
        default=1,
    )
    results = models.CharField(max_length=1000)


class veris_action_social_target(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vas_Id = models.ForeignKey(
        veris_action_social,
        on_delete=models.CASCADE,
        default=1,
    )
    target = models.CharField(max_length=1000)


######################################################################
# Veris Incident Action Information Tables - Misuse
######################################################################


class veris_action_misuse(models.Model):
    vamis_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    notes = models.CharField(max_length=1000, null=True)


class veris_action_misuse_variety(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vamis_Id = models.ForeignKey(
        veris_action_misuse,
        on_delete=models.CASCADE,
        default=1,
    )
    variety = models.CharField(max_length=200)


class veris_action_misuse_vector(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vamis_Id = models.ForeignKey(
        veris_action_misuse,
        on_delete=models.CASCADE,
        default=1,
    )
    vector = models.CharField(max_length=200)


class veris_action_misuse_results(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vamis_Id = models.ForeignKey(
        veris_action_misuse,
        on_delete=models.CASCADE,
        default=1,
    )
    results = models.CharField(max_length=1000)


class veris_action_misuse_target(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vamis_Id = models.ForeignKey(
        veris_action_misuse,
        on_delete=models.CASCADE,
        default=1,
    )
    target = models.CharField(max_length=1000)


######################################################################
# Veris Incident Action Information Tables - Physical
######################################################################


class veris_action_physical(models.Model):
    vap_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    notes = models.CharField(max_length=3000, null=True)


class veris_action_physical_variety(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vap_Id = models.ForeignKey(
        veris_action_physical,
        on_delete=models.CASCADE,
        default=1,
    )
    variety = models.CharField(max_length=200)


class veris_action_physical_vector(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vap_Id = models.ForeignKey(
        veris_action_physical,
        on_delete=models.CASCADE,
        default=1,
    )
    vector = models.CharField(max_length=200)


class veris_action_physical_location(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vap_Id = models.ForeignKey(
        veris_action_physical,
        on_delete=models.CASCADE,
        default=1,
    )
    location = models.CharField(max_length=1000)


class veris_action_physical_result(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vap_Id = models.ForeignKey(
        veris_action_physical,
        on_delete=models.CASCADE,
        default=1,
    )
    result = models.CharField(max_length=1000)


######################################################################
# Veris Incident Action Information Tables - Error
######################################################################


class veris_action_error(models.Model):
    vae_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    notes = models.CharField(max_length=1000, null=True)


class veris_action_error_variety(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vae_Id = models.ForeignKey(
        veris_action_error,
        on_delete=models.CASCADE,
        default=1,
    )
    variety = models.CharField(max_length=200)


class veris_action_error_vector(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vae_Id = models.ForeignKey(
        veris_action_error,
        on_delete=models.CASCADE,
        default=1,
    )
    vector = models.CharField(max_length=200)


class veris_action_error_result(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vae_Id = models.ForeignKey(
        veris_action_error,
        on_delete=models.CASCADE,
        default=1,
    )
    result = models.CharField(max_length=200)


######################################################################
# Veris Incident Action Information Tables - Environmental
######################################################################


class veris_action_environmental(models.Model):
    vaenv_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    notes = models.CharField(max_length=1000, null=True)


class veris_action_environmental_variety(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vaenv_Id = models.ForeignKey(
        veris_action_environmental,
        on_delete=models.CASCADE,
        default=1,
    )
    variety = models.CharField(max_length=200)


######################################################################
# Veris Incident Actor Information Tables
######################################################################


class veris_actor(models.Model):
    vat_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    actor_type = models.CharField(max_length=45)

    def __unicode__(self):
        return self.name


class veris_actor_motive(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vat_Id = models.ForeignKey(
        veris_actor,
        on_delete=models.CASCADE,
        default=1,
    )
    motive = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class veris_actor_variety(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vat_Id = models.ForeignKey(
        veris_actor,
        on_delete=models.CASCADE,
        default=1,
    )
    variety = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class veris_actor_origin(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vat_Id = models.ForeignKey(
        veris_actor,
        on_delete=models.CASCADE,
        default=1,
    )
    origin = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


######################################################################
# Veris Incident Asset Information Tables
######################################################################


class veris_asset(models.Model):
    vass_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    notes = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class veris_asset_variety(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vass_Id = models.ForeignKey(
        veris_asset,
        on_delete=models.CASCADE,
        default=1,
    )
    variety = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class veris_asset_ownership(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vass_Id = models.ForeignKey(
        veris_asset,
        on_delete=models.CASCADE,
        default=1,
    )
    ownership = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class veris_asset_management(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vass_Id = models.ForeignKey(
        veris_asset,
        on_delete=models.CASCADE,
        default=1,
    )
    management = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class veris_asset_hosting(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vass_Id = models.ForeignKey(
        veris_asset,
        on_delete=models.CASCADE,
        default=1,
    )
    hosting = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class veris_asset_accessibility(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vass_Id = models.ForeignKey(
        veris_asset,
        on_delete=models.CASCADE,
        default=1,
    )
    accessibility = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class veris_asset_cloud(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vass_Id = models.ForeignKey(
        veris_asset,
        on_delete=models.CASCADE,
        default=1,
    )
    cloud = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


######################################################################
# Veris Incident Impact Information Tables
######################################################################


class veris_impact(models.Model):
    vim_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    notes = models.CharField(max_length=1000)
    iso_currency_code = models.CharField(max_length=5)
    overall_amount = models.IntegerField()
    overall_min_amount = models.IntegerField()
    overall_max_amount = models.IntegerField()
    overall_rating = models.CharField(max_length=45, default="None")
    notes = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class veris_impact_loss(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    vim_Id = models.ForeignKey(
        veris_asset,
        on_delete=models.CASCADE,
        default=1,
    )
    entry = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


######################################################################
# Action Logging for Scripts
######################################################################


# Error Captures
class errorCapture(models.Model):
    incident_id = models.BigAutoField(primary_key=True)
    execution_type = models.TextField(blank=True)
    execution_object = models.CharField(max_length=1000)
    file_name = models.CharField(max_length=250)
    file_line = models.IntegerField(blank=True)
    date = models.DateField(blank=True)

    def __unicode__(self):
        return self.execution_object

    def __str__(self):
        return self.execution_object + "-" + self.file_name + "-" + str(self.date)


# Work Capture
class web_scraper_log(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    source = models.CharField(max_length=45)
    article_count = models.IntegerField()
    date = models.DateField(blank=True)

    def __unicode__(self):
        return self.date

    def __str__(self):
        return self.source + "-" + str(self.date)


######################################################################
# Capturing Interview Responses
######################################################################


# Error Captures
class interviewQuestions(models.Model):
    interviewee_Id = models.CharField(blank=False, max_length=100)
    question_1 = models.TextField(blank=False)
    question_2 = models.TextField(blank=False)
    question_3 = models.TextField(blank=False)
    question_4 = models.TextField(blank=False)
    question_5 = models.TextField(blank=False)
    question_6 = models.TextField(blank=False)
    question_7 = models.TextField(blank=False)
    question_8 = models.TextField(blank=False)
    question_9 = models.TextField(blank=False)
    question_10 = models.TextField(blank=False)
    date_created = models.DateField(blank=False, auto_now=True)

    def __unicode__(self):
        return self.name
