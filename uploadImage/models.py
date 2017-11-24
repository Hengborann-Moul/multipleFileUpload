# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast
import logging
import os
import random
import string

from django.db import models
from django.utils.timezone import now as timezone_now

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)


# Create your models here.


def create_random_string(length=30):

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])


def upload_to(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'my_uploads/{}_{}{}'.format(
        now.strftime("%Y/%m/%d/%Y%m%d%H%M%S"),
        create_random_string(),
        filename_ext.lower()
    )


class Image(models.Model):
    json_images = models.TextField(default='[]', blank=True)

    def __unicode__(self):
        img_len = len(ast.literal_eval(self.json_images))
        return str(img_len) + " total images"

    def __str__(self):
        img_len = len(ast.literal_eval(self.json_images))
        return str(img_len) + " total images"

