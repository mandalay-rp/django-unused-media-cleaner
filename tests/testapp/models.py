from django.db import models


class MediaModel(models.Model):
    file = models.FileField(upload_to="uploads/")
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.image.name if self.image else self.file.name
