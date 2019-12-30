import io
import hashlib
from PIL import Image
from PIL.ExifTags import TAGS
from photos import models
from datetime import datetime
import os
import sys
from django.conf import settings


def hash_image(photo_path):
    try:
        img = Image.open(photo_path)
    except:
        print('Error when taking hash of {}'.format(photo_path))
        print(sys.exc_info()[0])
        return ''
    md5 = hashlib.md5()

    # Assume all other images are jpegs.....
    if photo_path.split('.')[-1].lower() == 'png':
        mime_type = 'png'
    else:
        mime_type = 'jpeg'

    with io.BytesIO() as memf:
        img.save(memf, mime_type)
        data = memf.getvalue()
        md5.update(data)

    hex_value = md5.hexdigest()
    # print(hex_value)
    return hex_value


def get_DateTimeOriginal(path):
    img = Image.open(path)
    orig = ''
    # Get the DateTimeOriginal
    # check there is metadata
    md = img._getexif()
    if not isinstance(md, dict):
        return ''
    for tag, value in img._getexif().items():
        key = TAGS.get(tag, tag)
        if key == 'DateTimeOriginal':
            orig = value
            break
    
    # return orig as string if no stamp
    if orig != '':
        # Making massive assumptions on format
        # Year:month:day hr:min:sec
        date, time = orig.split(' ')
        if ':' in date:
            year,month,day = list(map(int, date.split(':')))
        elif '-' in date:
            year,month,day = list(map(int, date.split('-')))
            
        hour,minute,sec = list(map(int, time.split(':')))

        return datetime(year, month, day, hour, minute, sec, 0)
    else:
        return ''


def save_backup(name, orig_path):
    # Get the backup location stuff
    owner = name.split('/')[0]
    save_dir = os.path.join(settings.BACKUP_ROOT, owner)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Get an image to save
    img = Image.open(orig_path)
    backup_path = os.path.join(settings.BACKUP_ROOT, name)
    img.save(backup_path)
    return backup_path


def get_attribute(model, photo):
    qs = model.objects.filter(photo=photo)
    li = []
    for q in qs:
        li.append(str(q.atr))

    s = ', '.join(li)
    if len(li) == 0:
        s = ''
    return s


def get_html_attributes(photo, attributes=[]):
    # get created date if exists
    if photo.metadata:
        create_date = photo.create_date
    else:
        create_date = "Unknown"
    at_dict = {
        'owner': photo.owner,
        'event': get_attribute(models.EventTag, photo),
        'device': photo.device,
        'created': create_date,
        'uploaded': photo.upload_date,
    }
    if len(attributes) == 0:
        attributes = ['owner', 'event', 'device', 'created', 'uploaded']
    li = []
    for a in attributes:
        if at_dict[a] != '':
            li.append(['{}:'.format(a.capitalize()), 
                                    at_dict[a]])
    return li
