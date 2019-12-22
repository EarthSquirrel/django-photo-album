from django.core.management.base import BaseCommand
import os
from photos import models


class Command(BaseCommand):
    help = 'REQUIRES upload folder with names of people inside. It uploads \'
            the photos in each folder with the name as the owner.'

    def handle(self, *args, **options):
        for r,d,f in os.walk('upload'):
            people = d
            break

        for p in people:
            for r,d,f in os.walk(os.path.join('upload', p)):
                print(f)
                for ff in f:
                    pic = ff.lower()
                    if pic.endswith('jpg') or pic.endswith('png') or pic.endswith('jpeg'):
                        print("It's a picture!")
