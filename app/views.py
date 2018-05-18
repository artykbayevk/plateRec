# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseForbidden
from forms import ImageUploadForm
from models import ExampleModel
import shutil
import glob
import os
import cv2
import numpy as np
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return render(request,'index.html')

def upload_pic(request):

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # os.remove(file) for file in os.listdir('path/to/directory') if file.endswith('.png')
            for file in os.listdir(os.path.join(BASE_DIR, 'media', 'img')):
                if(file.endswith('.jpg')):
                    os.remove(os.path.join(BASE_DIR,'media','img',file))
            for file in os.listdir(os.path.join(BASE_DIR, 'static', 'img')):
                if(file.endswith('.jpg')):
                    os.remove(os.path.join(BASE_DIR,'static','img',file))
            m = ExampleModel()
            m.model_pic = form.cleaned_data['image']
            m.save()
            for file in os.listdir(os.path.join(BASE_DIR, 'media', 'img')):
                if(file.endswith('.jpg')):
                    shutil.move(os.path.join(BASE_DIR,'media','img',file), os.path.join(BASE_DIR,'media','img','main.jpg'))
                    shutil.copy(os.path.join(BASE_DIR,'media','img','main.jpg'),os.path.join(BASE_DIR,'static','img','main.jpg'))
            pathForImage = os.path.join(BASE_DIR, 'static', 'img','main.jpg')
            mainImage = cv2.imread(pathForImage)
            p = subprocess.Popen('alpr -c kz -p kz -j '+pathForImage, stdout = subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()



            return HttpResponse('image upload success'+ ' '+ pathForImage + ' '+ output)
    return HttpResponseForbidden('allowed only via POST')
