from django.db import models

class Make(models.Model):
    file = models.FileField('ファイル')

    def __str__(self):
        return self.file.url