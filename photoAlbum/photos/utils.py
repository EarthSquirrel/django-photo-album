import io
import hashlib
from PIL import Image


def hash_image(photo_path):
    img = Image.open(photo_path)
    md5 = hashlib.md5()

    with io.BytesIO() as memf:
        img.save(memf, 'jpeg')
        data = memf.getvalue()
        md5.update(data)

    hex_value = md5.hexdigest()
    print(hex_value)
    return hex_value
