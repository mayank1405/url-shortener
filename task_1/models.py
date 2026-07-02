from django.db import models



class Url_record(models.Model):

    longurl=models.URLField(max_length=600)
    shorturl=models.URLField(max_length=250)
    uuid_field=models.UUIDField()



# Create your models here.
