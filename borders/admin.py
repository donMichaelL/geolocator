from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Border
from .forms import BorderForm


@admin.register(Border)
class BorderAdmin(OSMGeoAdmin):
    form = BorderForm
    point_zoom = 11
    modifiable = False
