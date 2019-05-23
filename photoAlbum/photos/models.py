from django.db import models


class Photo(models.Model):
    photo_hash = models.CharField(max_length=500)
    name = models.CharField(max_length=700)
    document = models.ImageField()
    date = models.DateField(("Date"), auto_now_add=True)


class Animal(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.RESTRICT)
    mb = models.IntegerField(default=0)
    sampson = models.IntegerField(default=0)
    kitty = models.IntegerField(default=0)
    pumpkin = models.IntegerField(default=0)
    gisela = models.IntegerField(default=0)
    other = models.CharField(max_length=500, default='')


class Person(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.RESTRICT)
    peggy = models.IntegerField(default=0)
    britney = models.IntegerField(default=0)
    barbara = models.IntegerField(default=0)
    carman = models.IntegerField(default=0)
    ivan = models.IntegerField(default=0)
    erika = models.IntegerField(default=0)
    rachel = models.IntegerField(default=0)


class Places(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.RESTRICT)
    bozeman = models.IntegerField(default=0)
    great_falls = models.IntegerField(default=0)
