from django.contrib.gis.db import models

# Create your models here.
class Border(models.Model):
    name = models.CharField(max_length=50)
    point = models.PointField(blank=True, null=True)
    # mpoly = models.MultiPolygonField(blank=True, null=True)
    # poly = models.PolygonField(blank=True, null=True)


    def __str__(self):
        return self.name
39.5005, -0.47385