# coding:utf-8

from datetime import date, timedelta, datetime
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify as djslugify
from math import ceil
from random import choice
from string import lowercase, digits
from time import time
from unidecode import unidecode
import exceptions as exc
import os
import ujson

from PIL import Image as pyImage

def make_img_url_path(path, img_type):
    if not path:
        return ""
    return os.path.join(settings.MEDIA_URL, path.replace("orig", img_type))


def get_image_extension(img_obj):
    img = pyImage.open(img_obj)
    # yukarda geri sarma olmuyor
    img_obj.seek(0)
    return ".%s" % img.format.lower()


