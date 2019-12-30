from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
import os
import shutil
from photos import models, utils
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'REQUIRES upload folder with names of people inside. It uploads \
            the photos in each folder with the name as the owner.'

    def handle(self, *args, **options):
        # Get the model directories
        mods = {
            'Animal': models.Animal,
            #'Classifier': models.Classifier,
            'Event': [models.Event, models.EventTag]
            #'Location': models.Location,
            #'Person': models.Person
        }

        for mod in list(mods.keys()):
            print('\nWorking with folder: {}'.format(mod))
            # path to model folder
            model_path = os.path.join('sorting', mod)
            # Folders inside here are enteries for each model
            for root,dirs,files in os.walk(model_path):
                # These should be the names of each entery for model
                # print('Model enteries are: {}'.format(dirs))
                try:
                    dirs.remove('00-tagged')
                except ValueError:
                    pass
                try: 
                    dirs.remove('00-failed')
                except ValueError:
                    pass

                for dd in dirs:
                    # Make results folders paths
                    tagged = os.path.join(model_path, '00-tagged')
                    failed = os.path.join(model_path, '00-failed')
                    # get the entry for the model Model/Entry/photos
                    entry = mods[mod][0].objects.filter(name=dd)[0]
                    for r,d,f in os.walk(os.path.join(root, dd)):
                        print('*Tagging: {}:{}*'.format(mod, str(entry)))
                        total_tagged = 0
                        # itterate through each photo
                        entry_tagged = os.path.join(tagged, str(entry))
                        entry_failed = os.path.join(failed, str(entry))

                        for ff in f:
                            path = os.path.join(r, ff)
                            photo_hash = utils.hash_image(path)
                            photo = models.Photo.objects.filter(photo_hash=photo_hash)
                            # Check if photo is in db
                            if len(photo) > 0:
                                total_tagged += 1
                                # print('Creating tag for {}:{}'.format(str(entry), ff))
                                # create tag
                                mods[mod][1].objects.get_or_create(photo=photo[0], atr=entry)
                                # Move to tagged folder
                                if not os.path.exists(entry_tagged):
                                    os.makedirs(entry_tagged)
                                os.rename(path, os.path.join(entry_tagged, ff))
                            # Error not an image file
                            elif photo_hash == '':
                                print('{} could not be opened as img'.format(ff))
                                if not os.path.exists(entry_failed):
                                    os.makedirs(entry_failed)
                                os.rename(path, os.path.join(entry_failed, 'bad_{}'.format(ff)))
                                print('')
                            # Not in database
                            else:
                                print('{} not in database'.format(ff))
                                if not os.path.exists(entry_failed):
                                    os.makedirs(entry_failed)
                                # os.rename(path, os.path.join(entry_failed, ff))
                        if total_tagged > 0:
                            print('\tAdded {} photos'.format(total_tagged))
                break
            print('')
