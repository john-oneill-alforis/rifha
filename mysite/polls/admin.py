from django.contrib import admin

# Register your models here.

from .models import Question
from .models import trainingCorpus
from .models import textLabels
from .models import errorCapture


admin.site.register(Question)
admin.site.register(trainingCorpus)
admin.site.register(textLabels)
admin.site.register(errorCapture)
