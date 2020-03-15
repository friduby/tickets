from django.db import models

class Global(models.Model):
    counter = models.PositiveIntegerField(default=0)

    @staticmethod
    def get():
        ins = Global.objects.all()
        if ins.count() > 0:
            ins = ins.first()
        else:
            ins = Global.objects.create()
        return ins

class Request(models.Model):
    data1 = models.TextField(blank=True, null=True)
    data2 = models.TextField(blank=True, null=True)
    data3 = models.TextField(blank=True, null=True)