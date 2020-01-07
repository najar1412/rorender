from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'<{self.name}>'


class Machine(models.Model):
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    port = models.CharField(max_length=200)
    running = models.BooleanField(default=True)
    rendering = models.BooleanField(default=False)
    vray_running = models.BooleanField(default=False)
    backburner_running = models.BooleanField(default=False)
    corona_running = models.BooleanField(default=False)
    is_workstation = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    has_rhino = models.BooleanField(default=False)
    has_autocad = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'<{self.name}({self.ip})>'


