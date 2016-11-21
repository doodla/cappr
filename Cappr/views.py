import time
from base64 import decodebytes

from django.db.models import Case
from django.db.models import When
from django.shortcuts import render
from webcolors import hex_to_rgb

from .lib.utils import *


def index(request):
    return render(request, 'index.html', {'title': ''})


def get_image(request):
    return render(request, 'get_image.html', {'title': 'Upload Image'})


def view_result(request):
    img_data = request.POST.get('image')

    file_name = time.strftime("%Y%m%d_%H%M%S") + '.png'

    request.session['file_path'] = 'media/user/' + file_name
    # Write Base64 data to file.
    with open("media/user/" + file_name, "wb") as fh:
        fh.write(decodebytes(img_data.encode()))

    # Read bytes. TODO: Combine this and the step above?
    with open('media/user/' + file_name, 'rb') as f:
        img_data = f.read()

    # User's Accent
    hex_accent = get_accent_color(img_data)

    r, g, b = hex_to_rgb(hex_accent)
    rgb_accent = '{},{},{}'.format(r, g, b)

    # Get the caps in descending order of similarity
    order = get_matches(rgb_accent, settings.NUM_OF_RESULTS)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(order)])
    caps = Cap.objects.filter(pk__in=order).order_by(preserved)

    return render(request, 'view_result.html', {'title': 'Cappr', 'caps': caps})


def file_upload(request):
    file = request.FILES['pic']

    file_name = time.strftime("%Y%m%d_%H%M%S") + '.png'

    # Storing the file path in a session variable so we can use it when we need to cap the user.
    request.session['file_path'] = 'media/user/' + file_name

    with open('media/user/' + file_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # TODO: Combine this with the step above?
    with open('media/user/' + file_name, 'rb') as f:
        img_data = f.read()

    hex_accent = get_accent_color(img_data)

    r, g, b = hex_to_rgb(hex_accent)
    rgb_accent = '{},{},{}'.format(r, g, b)

    order = get_matches(rgb_accent, settings.NUM_OF_RESULTS)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(order)])
    caps = Cap.objects.filter(pk__in=order).order_by(preserved)

    return render(request, 'view_result.html', {'title': 'Cappr', 'caps': caps})
