from django.db import models

class UploadFile(models.Model):
    file = models.FileField('ファイル')

    def __str__(self):
        return self.file.url