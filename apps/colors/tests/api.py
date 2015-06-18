import json
import os

from django.test import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from ..models import ImageFile
from .base import make_image_file, make_color


class ImageFileUploadTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def get_sample_file(self, fname, content_type='image/jpeg'):
        with open(os.path.join(settings.APP_ROOT, 'data', fname), 'rb') as f:
            img_data = f.read()
            return SimpleUploadedFile(
                fname, img_data, content_type
            )

    def test_upload_jpeg_file(self):
        url = reverse('post-imagefile')
        data = {
            'image': self.get_sample_file('cobra.jpg', 'image/jpeg')
        }
        r = self.client.post(url, data=data)
        json_data = json.loads(r.content)
        self.assertIn('cobra.jpg', json_data)
        self.assertEqual(json_data['cobra.jpg']['success'], True)

        self.assertEqual(ImageFile.objects.count(), 1)

    def test_upload_png_file(self):
        url = reverse('post-imagefile')
        data = {
            'image': self.get_sample_file('1.png', 'image/png')
        }
        r = self.client.post(url, data=data)
        json_data = json.loads(r.content)
        self.assertIn('1.png', json_data)
        self.assertEqual(json_data['1.png']['success'], False)
        self.assertEqual(len(json_data['1.png']['errors']), 1)

        self.assertEqual(ImageFile.objects.count(), 0)

    def test_upload_no_file_data(self):
        url = reverse('post-imagefile')
        data = {}
        r = self.client.post(url, data=data)
        json_data = json.loads(r.content)
        self.assertEqual(json_data, {})
        self.assertEqual(ImageFile.objects.count(), 0)

    def test_upload_no_non_image_file(self):
        url = reverse('post-imagefile')
        data = {
            'file': SimpleUploadedFile('app.pdf', b'asd', 'tex/tpdf')
        }
        r = self.client.post(url, data=data)
        json_data = json.loads(r.content)
        self.assertIn('app.pdf', json_data)
        self.assertEqual(json_data['app.pdf']['success'], False)
        self.assertEqual(len(json_data['app.pdf']['errors']), 1)
        self.assertEqual(ImageFile.objects.count(), 0)

    def test_upload_multiple_files(self):
        url = reverse('post-imagefile')
        data = {
            'image1': self.get_sample_file('cobra.jpg', 'image/jpeg'),
            'image2': self.get_sample_file('onlywhite.jpg', 'image/jpeg'),
        }
        r = self.client.post(url, data=data)
        json_data = json.loads(r.content)
        self.assertIn('cobra.jpg', json_data)
        self.assertIn('onlywhite.jpg', json_data)
        self.assertEqual(json_data['cobra.jpg']['success'], True)
        self.assertEqual(json_data['onlywhite.jpg']['success'], True)

        self.assertEqual(ImageFile.objects.count(), 2)


class ImageListSearchTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def _prepare_test_data(self):
        image_file = make_image_file()
        image_file.save()
        color = make_color(image=image_file)
        color.save()

    def get_url(self, params=''):
        base_url = reverse('list-imagefile')
        return ''.join([base_url, params])

    def test_response_database_is_empty(self):
        url = self.get_url()
        r = self.client.get(self.get_url())
        json_data = json.loads(r.content)
        for key in ['previous', 'next', 'count', 'results']:
            self.assertIn(key, json_data)
        self.assertEqual(json_data['count'], 0)

    def test_response_database_is_not_empty(self):
        self._prepare_test_data()
        r = self.client.get(self.get_url())
        json_data = json.loads(r.content)
        self.assertIn('results', json_data)
        item = json_data['results'][0]

        for key in ['basename', 'source', 'created_at', 'colors', 'id']:
            self.assertIn(key, item)

        self.assertEqual(len(item['colors']), 1)
        self.assertEqual(item['colors'][0]['name'], 'white')
        self.assertEqual(item['colors'][0]['hex'], '#ffffff')
        self.assertEqual(item['basename'], 'test.jpg')
        self.assertEqual(json_data['count'], 1)

    def test_search_by_color_name(self):
        self._prepare_test_data()

        r = self.client.get(self.get_url('?color=white'))
        json_data = json.loads(r.content)
        self.assertEqual(json_data['count'], 1)

        r = self.client.get(self.get_url('?color=black'))
        json_data = json.loads(r.content)
        self.assertEqual(json_data['count'], 0)

    def test_search_by_hex(self):
        self._prepare_test_data()
        r = self.client.get(self.get_url('?hex=ffffff'))
        json_data = json.loads(r.content)
        self.assertEqual(json_data['count'], 1)

        r = self.client.get(self.get_url('?hex=FFFFFF'))
        json_data = json.loads(r.content)
        self.assertEqual(json_data['count'], 1)

        r = self.client.get(self.get_url('?hex=WSDAS'))
        json_data = json.loads(r.content)
        self.assertEqual(json_data['count'], 0)