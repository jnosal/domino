from django.db import models
from django.conf import settings

from .fields import ContentTypeRestrictedImageField


class Color(models.Model):
    name = models.CharField(
        blank=False, null=False,
        max_length=255, db_index=True
    )
    hex = models.CharField(
        max_length=255, db_index=True,
        blank=False, null=False,
    )
    r = models.IntegerField(blank=False, null=False)
    g = models.IntegerField(blank=False, null=False)
    b = models.IntegerField(blank=False, null=False)
    priority = models.IntegerField(blank=False, null=False, default=1)

    image = models.ForeignKey(
        'colors.ImageFile',
        blank=False, null=False,
        on_delete=models.CASCADE, db_index=True,
        related_name="colors", related_query_name="color"
    )

    def __unicode__(self):
        return u"{0} ({1})".format(
            self.name.capitalize(), self.hex
        )

    def __repr__(self):
        return self.__unicode__()

    class Meta:
        app_label = 'colors'


class ImageFile(models.Model):
    basename = models.CharField(
        blank=False, null=False,
        max_length=255, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = ContentTypeRestrictedImageField(
        content_types=settings.IMAGE_CONTENT_TYPES,
        upload_to='images/', blank=False, null=False
    )

    class Meta:
        app_label = 'colors'
        ordering = ['-created_at']

    def __unicode__(self):
        return u"{0}".format(
            self.basename
        )

    def __repr__(self):
        return self.__unicode__()