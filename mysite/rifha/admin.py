from django.contrib import admin

# Register your models here.

from .models import staff
from .models import staffRole

# Register your models here.


admin.site.register(staff)
admin.site.register(staffRole)
