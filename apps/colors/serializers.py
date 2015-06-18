from django.conf import settings
from rest_framework import serializers

from .models import ImageFile, Color


def check_content_type(value):
    if not value.content_type in settings.IMAGE_CONTENT_TYPES:
        raise serializers.ValidationError(u'Content Type not in {0}'.format(
            u", ".join(settings.IMAGE_CONTENT_TYPES)
        ))


class InputImageFileSerializer(serializers.Serializer):
    source = serializers.ImageField(validators=[check_content_type])


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ('name', 'hex', 'priority',)


class ImageFileSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True, read_only=True)

    class Meta:
        model = ImageFile
