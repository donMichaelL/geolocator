from django import forms
from django.contrib.gis.geos import Point

from .models import Border


class BorderForm(forms.ModelForm):
    latitude = forms.FloatField(required=True)
    longitude = forms.FloatField(required=True)

    class Meta:
        model = Border
        fields = ['name', 'longitude', 'latitude', 'point']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coordinates = self.initial.get('point', None)
        if isinstance(coordinates, Point):
            self.initial['longitude'], self.initial['latitude'] = coordinates.tuple
            self.fields['point'].widget.attrs['modifiable'] = False


    def clean(self):
        data = super().clean()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        data['point'] = Point(longitude, latitude)
        return data