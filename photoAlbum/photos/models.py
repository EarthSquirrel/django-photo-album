from django.db import models
from django.dispatch import receiver
from easy_thumbnails.fields import ThumbnailerImageField


class Photo(models.Model):
    photo_hash = models.CharField(max_length=500)
    date = models.DateField(("Date"), auto_now_add=True)
    document = models.ImageField()
    small_thumb = ThumbnailerImageField(resize_source=dict(size=(100, 100),
                                                           sharpen=True))
    medium_thumb = ThumbnailerImageField(resize_source=dict(size=(200, 200),
                                                            sharpen=True))
    large_thumb = ThumbnailerImageField(resize_source=dict(size=(400, 400),
                                                           sharpen=True))

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
    # TODO: Add in year with restrictions
    # year = models.IntegerField()
    def __str__(self):
        return self.name


# use for other things that aren't included (ex: memes)
class Classifier(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
