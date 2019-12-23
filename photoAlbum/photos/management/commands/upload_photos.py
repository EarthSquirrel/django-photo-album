from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
import os
from photos import models, utils


class Command(BaseCommand):
    help = 'REQUIRES upload folder with names of people inside. It uploads \
            the photos in each folder with the name as the owner.'

    def handle(self, *args, **options):
        for r,d,f in os.walk('upload'):
            people = d
            break

        for p in people:
            print('\n***Uploading photos from {}***'.format(p))
            person = models.Person.objects.filter(name__icontains=p)[0]
            print(person)
            
            for r,d,f in os.walk(os.path.join('upload', p)):
                print('files: ', f)
                for ff in f:
                    pic = ff.lower()
                    if pic.endswith('jpg') or pic.endswith('png') or pic.endswith('jpeg'):
                        # print("It's a picture!")
                        print('Uploading: {}'.format(ff))
                        path = os.path.join(r, ff)
                        # get image hash
                        img_hash = utils.hash_image(path)
                        photo = models.Photo.objects.create(photo_hash=img_hash, owner=person)
                        photo.document = ImageFile(open(path, 'rb'))
                        photo.document.name = ff
                        doc = photo.document
                        photo.small_thumb.save(name=doc.name, content=doc)
                        photo.medium_thumb.save(name=doc.name, content=doc)
                        photo.large_thumb.save(name=doc.name, content=doc)
                        photo.save() 
                        # TODO: Move picture to uploaded folder