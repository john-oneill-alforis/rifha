from django.contrib import admin

# Register your models here.

from .models import Question
from .models import trainingCorpus
from .models import textLabels
from .models import errorCapture
from .models import web_scraper_log


admin.site.register(Question)
admin.site.register(trainingCorpus)
admin.site.register(textLabels)
admin.site.register(errorCapture)
admin.site.register(web_scraper_log)
