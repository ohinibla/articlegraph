from django.db import models

# Create your models here.

class Site(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=1024)
    synopsis = models.CharField(max_length=2048)
    thumb_img = models.URLField(default='')
    
    def __str__(self):
        return self.title
    
class Link(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    address = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024)
    
    def __str__(self):
        return self.title