from django.db import models


class Photo(models.Model):
    photo_hash = models.CharField(max_length=500)
    document = models.ImageField()
    date = models.DateField(("Date"), auto_now_add=True)

    def __str__(self):
        return self.photo_hash


class Animal(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


# use for other things that aren't included (ex: memes)
class Classifier(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
