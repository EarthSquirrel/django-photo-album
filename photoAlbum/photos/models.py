from django.db import models
from django.dispatch import receiver


class Photo(models.Model):
    photo_hash = models.CharField(max_length=500)
    document = models.ImageField()
    date = models.DateField(("Date"), auto_now_add=True)

    def __str__(self):
        return self.photo_hash


@receiver(models.signals.post_delete, sender=Photo)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.document.delete(save=False)
    # instance.medium_thumb.delete(save=False)
    # instance.large_thumb.delete(save=False)


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
