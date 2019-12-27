from django.db import models
from django.dispatch import receiver
from easy_thumbnails.fields import ThumbnailerImageField
import os
import shutil
from django.conf import settings


class Animal(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def save(self, *args, **kwargs):
        os.mkdir('sorting/Animal/{}'.format(self.name))
        super(Animal, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def save(self, *args, **kwargs):
        os.mkdir('upload/{}'.format(self.name))
        os.mkdir('sorting/Person/{}'.format(self.name))
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Device(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def save(self, *args, **kwargs):
        for r,d,f in os.walk('upload'):
            for dd in d:
                base = os.path.join(r, dd)
                full = os.path.join(base, self.name)
                os.mkdir(full)
            break
        super(Device, self).save(*args, **kwargs)

    def __str__(self):
        return self.name




class Location(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def save(self, *args, **kwargs):
        os.mkdir('sorting/Location/{}'.format(self.name))
        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def save(self, *args, **kwargs):
        os.mkdir('sorting/Event/{}'.format(self.name))
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

# use for other things that aren't included (ex: memes)
class Classifier(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def save(self, *args, **kwargs):
        os.mkdir('sorting/Classifier/{}'.format(self.name))
        super(Classifier, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def thumb_directory_path(instance, filename):
    return 'thumbs/{}'.format(filename)


def owner_directory_path(instance, filename):
    return '{}/{}'.format(str(instance.owner), filename)


def backup_directory_path(instance, filename):
    return '{}/{}/{}'.format(settings.BACKUP_ROOT, str(instance.owner),
                             filename)


class Photo(models.Model):
    # Hash to make sure only uploaded once
    photo_hash = models.CharField(max_length=500, unique=True)
    # Keep track of dates
    upload_date = models.DateField(("Date"), auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    metadata = models.BooleanField(default=False)
    # Other metadata
    owner = models.ForeignKey(Person, on_delete=models.PROTECT)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    # Path to the backup location, hope this doesn't fail
    backup_path = models.TextField()
    # Keep all the photo files
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
    # check if owner folder exists
    deleted = '{}/deleted'.format(settings.MEDIA_ROOT)
    if not os.path.exists(deleted):
        os.mkdir(deleted)
    # check if owner exists
    owner = '{}/{}'.format(deleted, instance.owner)
    if not os.path.exists(owner):
        os.mkdir(owner)
    name = instance.document.name
    # TODO: REname deleted file in backups
    
    # show in backup file that the original has been deleted
    os.rename(instance.backup.path, 'deleted_{}'.format(instance.backup.path))
    
    # instance.document.delete(save=False)
    instance.small_thumb.delete(save=False)
    instance.medium_thumb.delete(save=False)
    instance.large_thumb.delete(save=False)


class EventTag(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    atr = models.ForeignKey(Event, on_delete=models.PROTECT)
