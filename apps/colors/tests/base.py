import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from ..models import Color, ImageFile


def make_color(**kwargs):
    base_data = {
        'r': 255,
        'g': 255,
        'b': 255,
        'hex': '#ffffff',
        'name': 'white'
    }
    base_data.update(kwargs)
    return Color(**base_data)


def make_image_file(**kwargs):
    with open(os.path.join(settings.APP_ROOT, 'data', 'test.jpg'), 'rb') as f:
        img_data = f.read()

    base_data = {
        'basename': 'test.jpg',
        'source': SimpleUploadedFile(
            'test.jpg', img_data, content_type='image/jpeg'
        )
    }
    base_data.update(kwargs)
    return ImageFile(**base_data)