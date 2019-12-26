import io
import hashlib
from PIL import Image
from PIL.ExifTags import TAGS
from photos import models
import datetime as dt


def hash_image(photo_path):
    img = Image.open(photo_path)
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
    for tag, value in img._getexif().items():
        key = TAGS.get(tag, tag)
        if key == 'DateTimeOriginal':
            orig = value
            break
    
    # return orig as string if no stamp
    if orig != '':
        return orig  # TODO: Convert to datetime object
    else:
        return ''


def get_attribute(model, photo):
    qs = model.objects.filter(photo=photo)
    li = []
    for q in qs:
        li.append(str(q.event))

    s = ', '.join(li)
    if len(li) == 0:
        s = 'No events'
    return s


def get_html_attributes(photo, attributes=[]):
    at_dict = {
        'owner': photo.owner,
        'event': get_attribute(models.EventTag, photo),
        'uploaded': photo.date,
    }
    if len(attributes) == 0:
        attributes = ['owner', 'event', 'uploaded']
    li = []
    for a in attributes:
        li.append(['{}:'.format(a.capitalize()), at_dict[a]])
    return li
