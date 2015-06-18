from django.db.models import ImageField
from django.forms import forms
from django.utils.translation import ugettext_lazy as _


class ContentTypeRestrictedImageField(ImageField):
    description = u"""
        ImageField that restricts files to certain content types.
        Setting content_types to None or blank lists does not force validation.
    """

    def __init__(self, content_types=None, *args, **kwargs):
        content_types = content_types if content_types else []
        self.content_types = content_types
        super(ContentTypeRestrictedImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedImageField, self).clean(*args, **kwargs)

        f = data.file

        try:
            content_type = f.content_type
            if self.content_types and not content_type in self.content_types:
                raise forms.ValidationError(_(u'Image type not supported.'))

        except AttributeError:
            pass

        return data