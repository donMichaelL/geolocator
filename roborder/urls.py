"""roborder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.gis.geos import Point
from borders.models import Border
from django.http import JsonResponse

import pyproj
class HomeView(TemplateView):
    template_name = "index.html"


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        point1 = Point(10.265271, 43.5337912)
        a = Border.objects.get(name="runadmin")
        a.point = point1
        a.save()
        return context

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     ath = Point(23.727539, 37.983810, srid=4326)
    #     thes = Point(22.943090, 40.634781, srid=4326)
    #     geod = pyproj.Geod(ellps='WGS84')
    #     angle1,angle2,distance = geod.inv(23.727539, 37.983810, 22.943090, 40.634781)
    #     dist = ath.distance(thes)
    #     print(distance)
    #     center = Border.objects.get(name="runadmin")
    #     center.point = Point(10.26605001465722,  43.53394028294053)
    #     center.save()
    #     # 10.26605001465722,  43.53394028294053
    #     return context
    #
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     point = Point(23.74008, 38.03619)
    #     point1 = Point(43.398991, 25.209454)
    #     second = Border.objects.get(id=2)
    #     p = second.point
    #     print(p)
    #     obj = Border.objects.filter(poly__contains=point)
    #     print(obj)
    #     print("HELLO")
    #     return context

# obj = Border.objects.filter(poly__contains=point)

class Observation:
    def __init__(self, latitude, longitude, distance):
        self.latitude = latitude
        self.longitude = longitude
        self.distance = distance


class CheckView(TemplateView):
    template_name = "index.html"

    def ciram_rulez(self, observations, vehicle_id, timestamp, p_timestamp):
        # getLevels?risks=risk1&distance=40
        # http://localhost:8000/check/?lon=-0.4728026&lat=39.5000516&p_lon=-0.4728766104653172&p_lat=39.50017239337358&vehicle_id=1&timestamp=1609756314926&p_timestamp=1609756319926
        import requests
        payload = []
        for idx, obs in enumerate(observations):
            payload.append(('risks', 'risk'+ str(idx+1)))
            payload.append(('distance', obs.distance))
            payload.append(('latitude', obs.latitude))
            payload.append(('longitude', obs.longitude))
        payload.append(('vehicle_id', vehicle_id))
        payload.append(('alert_start_time', timestamp))
        payload.append(('alert_end_time', p_timestamp))
        headers = {'accept': 'application/json'}
        r = requests.get('http://ciram-api:8080/getLevels', params=payload, headers=headers)
        print(r.url)
        return


    def get(self, request, *args, **kwargs):
        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)
        p_lon = request.GET.get('p_lon', None)
        p_lat = request.GET.get('p_lat', None)
        timestamp = request.GET.get('timestamp', None)
        p_timestamp = request.GET.get('p_timestamp', None)
        vehicle_id = request.GET.get('vehicle_id', None)
        point = Point(float(p_lon), float(p_lat))
        (lng2, lat2) = point.coords
        observations = []
        for border in Border.objects.all():
            center = border.point
            (lng1, lat1) = center.coords
            geod = pyproj.Geod(ellps='WGS84')
            az12,az21,dist = geod.inv(lng1,lat1,lng2,lat2)
            dist = dist*0.001
            observations.append(Observation(lat1, lng1, dist))
        print(dist)
        self.ciram_rulez(observations, vehicle_id, timestamp, p_timestamp)

        return JsonResponse({
                    'alert_uuid': 'bingo',
                })






urlpatterns = [
    path('', admin.site.urls),
    path('check/', CheckView.as_view(), name="check"),
    path('ena/', HomeView.as_view(), name="ena"),
]
