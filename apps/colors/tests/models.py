import os

from django.conf import settings
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Color, ImageFile
from .base import make_image_file, make_color


class ColorTestCase(TestCase):

    def test_color_properties(self):
        instance = make_color()
        self.assertEqual(instance.r, 255)
        self.assertEqual(instance.b, 255)
        self.assertEqual(instance.b, 255)
        self.assertEqual(instance.hex, '#ffffff')
        self.assertEqual(instance.name, 'white')
        self.assertEqual(instance.image_id, None)

    def test_insert_color_without_image(self):
        self.assertEqual(Color.objects.count(), 0)
        instance = make_color()
        self.assertRaises(ValidationError, lambda: instance.full_clean())

    def test_insert_color_with_image(self):
        self.assertEqual(Color.objects.count(), 0)
        image = make_image_file()
        image.save()
        instance = make_color(**{
            'image': image
        })
        instance.save()
        self.assertEqual(Color.objects.count(), 1)
        self.assertIn(instance, image.colors.all())


class ImageFileTestCase(TestCase):

    def get_file_data(self, fname='test.jpg'):
        with open(os.path.join(settings.APP_ROOT, 'data', fname), 'rb') as f:
            img_data = f.read()
            return img_data

    def test_image_file_properties(self):
        instance = make_image_file(source=None)
        self.assertEqual(instance.source, None)
        self.assertEqual(instance.colors.count(), 0)
        self.assertEqual(instance.basename, 'test.jpg')

    def test_insert_png_image(self):
        data = self.get_file_data(fname='1.png')
        source = SimpleUploadedFile('file.png', data, 'image/png')
        image_file = make_image_file(source=source)
        self.assertRaises(ValidationError, lambda: image_file.full_clean())

    def test_insert_jpeg_image(self):
        self.assertEqual(ImageFile.objects.count(), 0)
        data = self.get_file_data(fname='test.jpg')
        source = SimpleUploadedFile('test.jpg', data, 'image/jpeg')
        image_file = make_image_file(source=source)
        image_file.save()
        self.assertNotEqual(image_file.source, None)
        self.assertEqual(ImageFile.objects.count(), 1)

    def test_insert_without_source_image_fails(self):
        image_file = make_image_file(source=None)
        self.assertRaises(ValidationError, lambda: image_file.full_clean())

    def test_create_image_file_with_colors(self):
        image_file = make_image_file()
        image_file.save()
        color1 = make_color(name='white', image=image_file)
        color2 = make_color(name='red', image=image_file)
        color1.save()
        color2.save()
        image_file = ImageFile.objects.get()
        self.assertEqual(image_file.colors.count(), 2)
        self.assertIn(color1, image_file.colors.all())
        self.assertIn(color2, image_file.colors.all())