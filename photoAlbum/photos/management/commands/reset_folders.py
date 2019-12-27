from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
import os
import shutil
from photos import models, utils
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Reset the database and delete all of the folders'

    def create_subfolders(self, path, model):
        mods = model.objects.all()
        for m in mods:
            os.mkdir(os.path.join(path, str(m)))

    def handle(self, *args, **options):
        # reset sorting
        shutil.rmtree('sorting')
        os.mkdir('sorting')
        # Animal
        path = 'sorting/Animal'
        os.mkdir(path)
        self.create_subfolders(path, models.Animal)
        # Classifier
        path = 'sorting/Classifier'
        os.mkdir(path)
        self.create_subfolders(path, models.Classifier)
        # Event
        path = 'sorting/Event'
        os.mkdir(path)
        self.create_subfolders(path, models.Event)
        # Location
        path = 'sorting/Location'
        os.mkdir(path)
        self.create_subfolders(path, models.Location)
        # Person
        path = 'sorting/Person'
        os.mkdir(path)
        self.create_subfolders(path, models.Person)

        # reset upload
        for r,d,f in os.walk('upload'):
            for dd in d:
                shutil.rmtree(os.path.join('upload', dd))
            break
        # Make person folders
        self.create_subfolders('upload', models.Person)
        # Make devices for each person
        for person in models.Person.objects.all():
            path = 'upload/{}'.format(str(person))
            self.create_subfolders(path, models.Device)

