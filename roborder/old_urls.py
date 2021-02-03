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


class CheckView(TemplateView):
    template_name = "index.html"

    def ciram_rulez(self, value):
        # getLevels?risks=risk1&distance=40
        # [{"name":"risk1","risk":"high","impact":"medium","vulnerability":"high","threat":"high"}]
        import requests
        payload = [('risks', "risk1"), ('distance', value)]
        headers = {'accept': 'application/json'}
        r = requests.get('http://ciram-api:8080/getLevels', params=payload, headers=headers)
        return r.json()[0]


    def get(self, request, *args, **kwargs):
        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)
        p_lon = request.GET.get('p_lon', None)
        p_lat = request.GET.get('p_lat', None)
        vehicle_id = request.GET.get('vehicle_id', None)
        point = Point(float(p_lon), float(p_lat))
        (lng2, lat2) = point.coords
        center = Border.objects.get(name="runadmin").point
        (lng1, lat1) = center.coords
        print(p_lon, p_lat)
        (lng2, lat2) = point.coords
        geod = pyproj.Geod(ellps='WGS84')
        az12,az21,dist = geod.inv(lng1,lat1,lng2,lat2)
        dist = dist*0.001
        print("EDW")
        json_message = self.ciram_rulez(dist)

        return JsonResponse({
                    'alert_uuid': 'bingo',
                    'alert_level': json_message['risk'],
                    'alert_title': "Risk Models Alert",
                    'alert_text': json_message['risk'],
                    'alert_category': 'Incident Alert',
                    'alert_start_time': "",
                    'alert_source': "Risk Models",
                    'location': {
                        'type': "Point",
                        'coordinates': [p_lon, p_lat]
                    },
                    'vehicle_id': vehicle_id,
                    'ciram_details' : {
                        'impact': json_message['impact'],
                        'threat': json_message['threat'],
                        'vulnerability': json_message['vulnerability'],
                    }
                })






urlpatterns = [
    path('', admin.site.urls),
    path('check/', CheckView.as_view(), name="check"),
    path('ena/', HomeView.as_view(), name="ena"),
]
