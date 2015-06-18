import logging
import time

from django.conf import settings
from colorthief import ColorThief
import webcolors

from .models import ImageFile, Color
from .tasks import ImageColorTask


logger = logging.getLogger('domino')

HEX_MODE = 'hex'
NAME_MODE = 'name'


def get_closest_color(requested_color):
    min_colours = {}

    for key, name in webcolors.css3_hex_to_names.iteritems():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colours[(rd + gd + bd)] = name

    return min_colours[min(min_colours.keys())]


def get_color_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError as e:
        closest_name = get_closest_color(requested_colour)
        actual_name = None
    return actual_name, closest_name


def extract_and_save_colors(image_file, Extractor):
    """
        Given image file function extracts top colors from pallette
        and persists them in database saving: color name, (r, g, b) info
        and hex color name.
    """

    results = []
    mode = settings.IMAGE_COLOR_PERSIST_MODE

    helper = Extractor(image_file.source.file)
    palette = helper.get_palette(settings.IMAGE_VITAL_COLORS_COUNT)

    # if we are in hex mode
    # we are limiting results to unique r, g, b triplets that occur
    if mode == HEX_MODE:
        palette = [_ for _ in set(palette)]

    for index, triplet in enumerate(palette):
        hex_ = webcolors.rgb_to_hex(triplet)
        actual, closest = get_color_name(triplet)
        name = actual if actual else closest
        priority = index + 1
        color = Color(**{
            'r': triplet[0],
            'g': triplet[1],
            'b': triplet[2],
            'hex': hex_.lower(),
            'name': name,
            'image': image_file,
            'priority': priority
        })
        results.append(color)

    # if we are in name mode
    # we are limiting results to unique color names that occur
    if mode == NAME_MODE:
        colors, names = [], set()

        for c in results:
            if not c.name in names:
                names.add(c.name)
                colors.append(c)

    else:
        colors = results

    Color.objects.bulk_create(colors)
    return colors


class ImageColorExtractor(object):
    SYNC_MODE = 'sync'
    ASYNC_MODE = 'async'

    def __init__(self, source, mode=settings.IMAGE_EXTRACTION_MODE):
        self.source = source
        self.mode = mode

    def get_extractor(self):
        return ColorThief

    def get_handler(self):
        return extract_and_save_colors

    def get_image_instance(self):
        return ImageFile.objects.create(**{
            'basename': self.source.name,
            'source': self.source
        })

    def run(self):
        logger.info(u"Running {0} in {1} mode.".format(
            self.__class__.__name__, self.mode
        ))

        tic = time.time()
        image_file = self.get_image_instance()
        handler = self.get_handler()
        ColorExtractor = self.get_extractor()

        if self.mode == self.SYNC_MODE:
            # run handler in sync mode
            handler(image_file=image_file, Extractor=ColorExtractor)

        if self.mode == self.ASYNC_MODE:
            # schedule task which will run handler asynchronously
            async_task = ImageColorTask()
            args = (handler, image_file.id, ColorExtractor)
            async_task.apply_async(args=args)

        toc = time.time()
        logger.info(u'Processing took %0.3f ms' % ((toc - tic) * 1000.0, ))