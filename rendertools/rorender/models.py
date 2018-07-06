from django.db import models

class Machine(models.Model):
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    port = models.IntegerField()
    running = models.BooleanField(default=True)
    vray_running = models.BooleanField(default=True)
    corona_running = models.BooleanField(default=True)

    def __str__(self):
        return f'<{self.name}({self.ip})>'