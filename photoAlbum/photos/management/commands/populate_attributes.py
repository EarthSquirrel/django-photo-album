from django.core.management.base import BaseCommand
import json
from photos import models


class Command(BaseCommand):
    help = 'REQUIRES attributes.json. Will create models of each kind for \
            in the json file'

    def handle(self, *args, **options):
        with open('attributes.json') as json_file:
            attribs = json.load(json_file)
            print('Creating People!')
            try:
                for p in attribs['people']:
                    models.Person.objects.create(name=p)
                    print('Created person: {}'.format(p))
            except KeyError:
                print('attributes.json key error. Missing Person')
            print('\nCreating Animals')
            try:
                for p in attribs['animals']:
                    models.Animal.objects.create(name=p)
                    print('Created animal: {}'.format(p))
            except KeyError:
                print('attributes.json key error. Missing Animal')
            print('\nCreating Events!')
            try:
                for p in attribs['events']:
                    models.Event.objects.create(name=p)
                    print('Created event: {}'.format(p))
            except KeyError:
                print('attributes.json key error. Missing Event')
            print('\nCreating Classifiers!')
            try:
                for p in attribs['classifiers']:
                    models.Classifier.objects.create(name=p)
                    print('Created classifier: {}'.format(p))
            except KeyError:
                print('attributes.json key error. Missing Classifier')
