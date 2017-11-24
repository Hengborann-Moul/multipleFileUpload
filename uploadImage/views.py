# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import random
import string

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from uploadImage.models import Image
from .forms import ImageForm

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


# Create your views here.
def gen_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for x in range(length))


def file_upload_handler(image, filename):
    try:
        upload_dir = os.path.join(settings.BASE_DIR, 'media/accommodation/')
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)

    except OSError:
        logger.debug('Get os error while create folder')
        return None

    except:
        logger.debug('Generate error while create folder')
        return None

    def process_upload():
        file_string_name = gen_random_string(24)
        upload_file_path = upload_dir + file_string_name + '.' + str(filename).split('.')[-1]
        if not os.path.exists(upload_file_path):

            with open(upload_file_path, 'wb+') as fs:
                if image.multiple_chunks():
                    for chunk in image.chunks():
                        fs.write(chunk)
                else:
                    string_buffer = image.read()
                    fs.write(string_buffer)

            return upload_file_path
        else:
            process_upload()

    return process_upload()


def index(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        # form = ImageForm(request.POST, request.FILES)
        image_dict = request.FILES.getlist('images')
        img_array = list()
        contexts = dict()
        for item in image_dict:
            destination = file_upload_handler(item, item.name)
            img_array.append(destination)
            logging.debug(type(destination))
        contexts.update({'images': img_array})
        Image.objects.create(json_images=str(img_array))
        logger.debug(contexts)
        return JsonResponse(contexts)

    else:
        form = ImageForm()
        images = Image.objects.all()
        return render(request, 'index.html', {'form': form, 'images': images})
