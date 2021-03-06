# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import datetime
import io
import json
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from restapi.models import AnnotatedRecording, DemographicInformation
from rest_framework.decorators import api_view

END_OF_FILE = 6236

# get_ayah gets the surah num, ayah num, and text of a random ayah of a specified maximum length
@api_view(['GET', 'POST'])
def get_ayah(request, line_length=200):

    # user tracking - ensure there is always a session key
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Get random line
    with io.open('data.json', 'r', encoding='utf-8') as f:
        lines = json.load(f)
        f.close()

    # Parse line and add hash
    surah = request.data['surah'] if request.method == 'POST' else str(
        random.randint(1, 114))
    ayah = request.data['ayah'] if request.method == 'POST' else str(
        random.randint(1, len(lines[surah].keys())))
    line = lines[surah][ayah]
    image_url = static('img/ayah_images/'+str(surah)+"_"+str(ayah)+'.png')
    hash = random.getrandbits(32)

    # Format as json, and save row in DB
    result = {"surah": surah, "ayah": ayah, "line": line, "hash": hash,
              "session_id": session_key, "image_url": image_url}

    return JsonResponse(result)

################################################################################
############################## static page views ###############################
################################################################################
def index(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    recording_count = AnnotatedRecording.objects.filter(file__gt='', file__isnull=False).count()
    if recording_count > 1000:
       recording_count -= 1000  # because roughly our first 1,000 were test recordings
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    
    if DemographicInformation.objects.filter(session_id=session_key).exists():
        ask_for_demographics = False
    else:
        ask_for_demographics = True

    daily_count = AnnotatedRecording.objects.filter(
        timestamp__gt=yesterday).exclude(file__isnull=True).count()

    return render(request, 'audio/index.html', {'recording_count':recording_count, 
        'daily_count':daily_count, 'ask_for_demographics':ask_for_demographics})

def about(request):
    recording_count = AnnotatedRecording.objects.filter(file__gt='', file__isnull=False).count()
    if recording_count > 1000:
       recording_count -= 1000  # because roughly our first 1,000 were test recordings
    return render(request, 'audio/about.html', {'recording_count': recording_count})

def privacy(request):
    return render(request, 'audio/privacy.html', {})

def mobile_app(request):
    recording_count = AnnotatedRecording.objects.filter(file__gt='', file__isnull=False).count()
    if recording_count > 1000:
        recording_count -= 1000
    return render(request, 'audio/mobile_app.html', {"recording_count": recording_count})
