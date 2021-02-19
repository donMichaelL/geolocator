from django.contrib import admin

from .models import Border
from .forms import BorderForm


class BorderAdmin(admin.ModelAdmin):
    form = BorderForm

admin.site.register(Border, BorderAdmin)
# Register your models here.
