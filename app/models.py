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