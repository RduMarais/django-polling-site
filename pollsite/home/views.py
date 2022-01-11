from django.shortcuts import render, get_object_or_404
from .models import TeamMember

import yaml
from django.utils import timezone
import os


def index(request):
    # NOTE PUT ABSOLUTE PATH OF homePage.yaml here
    with open('/Users/romain/Stratus/info/server/tests_beekast/django-polling-site/pollsite/home/homePage.yaml', 'r') as file:
        homePageElements = yaml.full_load(file)
    team = TeamMember.objects.order_by('title')
    context = {'hpe': homePageElements, 'team': team}
    return render(request, 'home/index', context)

# We absolutely do not need this
def opnsrc(request):
    now = timezone.now()
    context = {'now': now}
    return render(request, 'home/license', context)
