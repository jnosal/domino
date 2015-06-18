from __future__ import absolute_import

from celery import Task
from celery.utils.log import get_task_logger

from .models import ImageFile
logger = get_task_logger(__name__)


class ImageColorTask(Task):

    def run(self, handler, image_pk, Extractor, **kwargs):
        try:
            image_file = ImageFile.objects.get(id=image_pk)
        except ImageFile.DoesNotExist:
            logger.error(u"ImageFile with id: {0} does not exist.".format(
                image_pk
            ))
        else:
            handler(image_file=image_file, Extractor=Extractor)