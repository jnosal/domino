import os

from colorthief import ColorThief
from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import ImageFile
from ..services import extract_and_save_colors


class ColorThiefTestCase(TestCase):

    def test_get_pallette_from_image_one(self):
        with open(os.path.join(settings.APP_ROOT, 'data', 'test.jpg'), 'rb') as f:
            image_file = ImageFile.objects.create(**{
                'basename': 'test.jpg',
                'source': SimpleUploadedFile(
                    'test.jpg', f.read(), 'image/jpeg'
                )
            })
            colors = extract_and_save_colors(
                image_file=image_file, Extractor=ColorThief
            )
            self.assertEqual(len(colors), settings.IMAGE_VITAL_COLORS_COUNT)
            names = [c.name for c in colors]
            self.assertIn('steelblue', names)
            self.assertIn('burlywood', names)
            self.assertIn('darkslategray', names)
            self.assertIn('darkolivegreen', names)
            self.assertIn('lightsteelblue', names)

    def test_get_pallette_from_image_two(self):
        with open(os.path.join(settings.APP_ROOT, 'data', 'cobra.jpg'), 'rb') as f:
            image_file = ImageFile.objects.create(**{
                'basename': 'test.jpg',
                'source': SimpleUploadedFile('cobra.jpg', f.read(), 'image/jpeg')
            })
            colors = extract_and_save_colors(
                image_file=image_file, Extractor=ColorThief
            )
            self.assertEqual(len(colors), settings.IMAGE_VITAL_COLORS_COUNT)
            names = [c.name for c in colors]
            self.assertIn('crimson', names)
            self.assertIn('whitesmoke', names)
            self.assertIn('lightcoral', names)
            self.assertIn('sienna', names)
            self.assertIn('tan', names)

    @override_settings(IMAGE_COLOR_PERSIST_MODE='name')
    def test_get_pallette_from_pure_white_image_with_color_name_mode(self):
        with open(os.path.join(settings.APP_ROOT, 'data', 'onlywhite.jpg'), 'rb') as f:
            image_file = ImageFile.objects.create(**{
                'basename': 'test.jpg',
                'source': SimpleUploadedFile(
                    'onlywhite.jpg', f.read(), 'image/jpeg'
                )
            })
            colors = extract_and_save_colors(
                image_file=image_file, Extractor=ColorThief
            )
            self.assertEqual(len(colors), 1)
            names = [c.name for c in colors]
            self.assertIn('snow', names)

    @override_settings(IMAGE_COLOR_PERSIST_MODE='hex')
    def test_get_pallette_from_pure_white_image_with_color_hex_mode(self):
        with open(os.path.join(settings.APP_ROOT, 'data', 'onlywhite.jpg'), 'rb') as f:
            image_file = ImageFile.objects.create(**{
                'basename': 'test.jpg',
                'source': SimpleUploadedFile(
                    'onlywhite.jpg', f.read(), 'image/jpeg'
                )
            })
            colors = extract_and_save_colors(
                image_file=image_file, Extractor=ColorThief
            )
            self.assertEqual(len(colors), 2)
            names = [c.name for c in colors]
            self.assertIn('snow', names)

    def test_get_pallette_no_extractor(self):
        with open(os.path.join(settings.APP_ROOT, 'data', 'cobra.jpg'), 'rb') as f:
            image_file = ImageFile.objects.create(**{
                'basename': 'test.jpg',
                'source': SimpleUploadedFile('cobra.jpg', f.read(), 'image/jpeg')
            })
            self.assertRaises(TypeError, lambda: extract_and_save_colors(
                image_file=image_file, Extractor=None
            ))

    def test_get_pallette_no_image(self):
        self.assertRaises(AttributeError, lambda: extract_and_save_colors(
            image_file=None, Extractor=ColorThief
        ))