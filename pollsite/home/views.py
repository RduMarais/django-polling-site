from django.shortcuts import render, get_object_or_404
from .models import TeamMember

import yaml
from django.utils import timezone
from django.conf import settings
import os

# In a cloned deployment, you should use these views to customize the home page
# In an app deployment, on the poll app is installed to your preexisting main view

def index(request):
    # NOTE PUT PATH OF homePage.yaml here
    # WHYYYYYYY
    with open(os.path.join(settings.BASE_DIR, 'home/homePage.yaml'), 'r') as file:
        homePageElements = yaml.full_load(file)
    team = TeamMember.objects.order_by('title')
    context = {'hpe': homePageElements, 'team': team}
    return render(request, 'home/index', context)

# We absolutely do not need this
def opnsrc(request):
    return render(request, 'home/license', {})
