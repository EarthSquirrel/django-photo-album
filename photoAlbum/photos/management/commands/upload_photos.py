from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
import os
from photos import models, utils
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'REQUIRES upload folder with names of people inside. It uploads \
            the photos in each folder with the name as the owner.'

    def create_photo(self, ff, path, per, dev):
        person = models.Person.objects.filter(name__icontains=per)[0]
        device = models.Device.objects.filter(name__icontains=dev)[0]
        # get image hash
        img_hash = utils.hash_image(path)
        if img_hash == '':
            print('Error not a readable image for hasing')
            print('\t{}'.format(path))
            return False
        try:
            photo = models.Photo.objects.create(photo_hash=img_hash, owner=person,
                                                device=device)
            photo.document = ImageFile(open(path, 'rb'))
            photo.document.name = ff
            doc = photo.document
            create_date = utils.get_DateTimeOriginal(path)
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
        return True
    
    

    def handle(self, *args, **options):
        for r,d,f in os.walk('upload'):
            people = d
            break

        for p in people:
            person_path = os.path.join('upload', p)
            
            for r,d,f in os.walk(person_path):
                devices = [os.path.join(r, dd) for dd in d]
                break
            
            for device in devices:
                dev = device.split('/')[-1]
                for r,d,f in os.walk(device):
                    # Uploaded path
                    mov_loc = os.path.join(device, 'uploaded')
                    # error folder path
                    error_path = os.path.join(device, 'error')
                    # remove mac .DS_Store from list
                    try:
                        f.remove('.DS_Store')
                    except ValueError:
                        pass
                    # Only print if there are pictures here
                    if len(f) > 0:
                        print('\n***Uploading photos from {},{}***'.format(p,dev))
                        # Make uploaded folder
                        if not os.path.exists(mov_loc):
                            os.mkdir(mov_loc)
                    
                    for ff in f:
                        pic = ff.lower()
                        # print("It's a picture!")
                        print('Uploading: {}'.format(ff))
                        path = os.path.join(r, ff)
                        created = self.create_photo(ff, path, p, dev) 
                        # move photo to uploaded folder
                        if created:
                            os.rename(path, os.path.join(mov_loc, ff))
                        else:
                            if not os.path.exists(error_path):
                                os.mkdir(error_path)
                            os.rename(path, os.path.join(error_path, ff))
                    break
