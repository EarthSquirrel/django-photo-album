from django.core.management.base import BaseCommand
import os
from photos import models


class Command(BaseCommand):
    help = 'REQUIRES attributes.json. Will create models of each kind for \
            in the json file'

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
