from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
import os
from photos import models, utils
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'REQUIRES upload folder with names of people inside. It uploads \
            the photos in each folder with the name as the owner.'

    def handle(self, *args, **options):
        for r,d,f in os.walk('upload'):
            people = d
            break

        for p in people:
            person = models.Person.objects.filter(name__icontains=p)[0]
            
            person_path = os.path.join('upload', p)
            uploaded = os.path.join(person_path, 'uploaded')

            if not os.path.exists(uploaded):
                os.mkdir(uploaded)

            for r,d,f in os.walk(person_path):
                try:
                    f.remove('.DS_Store')
                except ValueError:
                    pass
                if len(f) > 0:
                    print('\n***Uploading photos from {}***'.format(p))
                # print('files: ', f)
                for ff in f:
                    pic = ff.lower()
                    if pic.endswith('jpg') or pic.endswith('png') or pic.endswith('jpeg'):
                        # print("It's a picture!")
                        print('Uploading: {}'.format(ff))
                        path = os.path.join(r, ff)
                        # get image hash
                        img_hash = utils.hash_image(path)
                        try:
                            photo = models.Photo.objects.create(photo_hash=img_hash, owner=person)
                            photo.document = ImageFile(open(path, 'rb'))
                            photo.document.name = ff
                            doc = photo.document
                            create_date = utils.get_DateTimeOriginal(path)
                            create_date = ''
                            if create_date != '':
                                photo.create_date = create_date
                                photo.metadata = True
                            # create name with owner in it
                            name = '{}/{}'.format(str(person), doc.name)
                            photo.backup_path = utils.save_backup(name, path)
                            photo.small_thumb.save(name=doc.name, content=doc)
                            photo.medium_thumb.save(name=doc.name, content=doc)
                            photo.large_thumb.save(name=doc.name, content=doc)
                            photo.save()
                        except IntegrityError:
                            p = models.Photo.objects.get(photo_hash=img_hash)
                            print('**FAILED: duplicates id {}'.format(p.id))

                        # move photo to uploaded folder
                        os.rename(path, os.path.join(uploaded, ff))
                break
