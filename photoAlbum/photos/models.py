from django.db import models


class Photo(models.Model):
    photo_hash = models.CharField(max_length=500)
    document = models.ImageField()
    date = models.DateField(("Date"), auto_now_add=True)

"""
class AnimalMB(models.Model):
    photo = models.ForeignKey(Photo, on_delete-models.PROTECT)


class AnimalSampson(models.Model):
    photo = models.ForeignKey(Photo, on_delete-models.PROTECT)


class AnimalKitty(models.Model):
    photo = models.ForeignKey(Photo, on_delete-models.PROTECT)


class AnimalPumpkin(models.Model):
    photo = models.ForeignKey(Photo, on_delete-models.PROTECT)


class Animal(models.Model):
    photo = models.ForeignKey(Photo, on_delete-models.PROTECT)

class Animal(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.PROTECT)
    mb = models.IntegerField(default=0)
    sampson = models.IntegerField(default=0)
    kitty = models.IntegerField(default=0)
    pumpkin = models.IntegerField(default=0)
    gisela = models.IntegerField(default=0)
    other = models.CharField(max_length=500, default='')

"""

class Animal(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Sampson(Animal):
    pass

class Korra(Animal):
    pass


class MB(Animal):
    pass


class Pumpkin(Animal):
    pass



class Person(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.PROTECT)

    class Meta:
        abstract = True

class Peggy(Person):
    pass

class Carman(Person):
    pass


"""
class PersonOld(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.PROTECT)
    peggy = models.IntegerField(default=0)
    britney = models.IntegerField(default=0)
    barbara = models.IntegerField(default=0)
    carman = models.IntegerField(default=0)
    ivan = models.IntegerField(default=0)
    erika = models.IntegerField(default=0)
    rachel = models.IntegerField(default=0)


class Places(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.PROTECT)
    bozeman = models.IntegerField(default=0)
    great_falls = models.IntegerField(default=0)

"""
