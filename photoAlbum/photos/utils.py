import io
import hashlib
from PIL import Image


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
    print(hex_value)
    return hex_value
