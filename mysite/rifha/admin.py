from django.contrib import admin

# Register your models here.

from .models import staff
from .models import staffRole
from .models import assets
from .models import assetsTypes
from .models import processes


# Register your models here.

admin.site.register(staff)
admin.site.register(staffRole)
admin.site.register(assets)
admin.site.register(assetsTypes)
admin.site.register(processes)
