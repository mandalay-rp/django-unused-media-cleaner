from django.db import models


class MediaModel(models.Model):
    file = models.FileField(upload_to="uploads/")
    image = models.ImageField(upload_to="images/", blank=True, null=True)

