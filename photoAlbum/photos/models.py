from django.db import models
from django.dispatch import receiver
from easy_thumbnails.fields import ThumbnailerImageField
import os



class Animal(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


# TODO: Add folder to upload folder when a person is added
class Person(models.Model):
    name = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        os.mkdir('upload/{}'.format(self.name))
        os.mkdir('sorting/Person/{}'.format(self.name))
        super(Person, self).save(*args, **kwargs)

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

def thumb_directory_path(instance, filename):
    return 'thumbs/{}'.format(filename)


def owner_directory_path(instance, filename):
    return '{}/{}'.format(str(instance.owner), filename)


class Photo(models.Model):
    photo_hash = models.CharField(max_length=500)
    date = models.DateField(("Date"), auto_now_add=True)
    owner = models.ForeignKey(Person, on_delete=models.PROTECT)
    document = models.ImageField(upload_to=owner_directory_path)
    small_thumb = ThumbnailerImageField(upload_to=thumb_directory_path,
                                        resize_source=dict(size=(100, 100),
                                                           sharpen=True))
    medium_thumb = ThumbnailerImageField(upload_to=thumb_directory_path,
                                         resize_source=dict(size=(350, 350),
                                                            sharpen=True))
    large_thumb = ThumbnailerImageField(upload_to=thumb_directory_path,
                                        resize_source=dict(size=(900, 900),
                                                           sharpen=True))
    
    def __str__(self):
        return self.photo_hash


@receiver(models.signals.post_delete, sender=Photo)
def post_delete_file(sender, instance, *args, **kwargs):
    instance.document.delete(save=False)
    instance.small_thumb.delete(save=False)
    instance.medium_thumb.delete(save=False)
    instance.large_thumb.delete(save=False)


class EventTag(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
