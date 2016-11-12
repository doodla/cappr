from django.db.models import Case
from django.db.models import When
from django.shortcuts import render, redirect
from webcolors import hex_to_rgb

from CapFinder.lib.pilow import get_merged_image
from .lib.utils import *

_key_accent = '00ddd41708ea42b2b6afdc73b574d2d7'
_maxNumRetries = 10
_url_accent = 'https://api.projectoxford.ai/vision/v1/analyses'

_imgur_client = '4d6957ec71171dd'
_imgur_secret = '0baa0295d9e233347e487693fd4717604d847911'


def add_caps(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        url = request.POST.get('url')
        price = request.POST.get('price')
        emotion = request.POST.get('emotion')

        params = {'visualFeatures': 'Color,Categories'}

        headers = {'Ocp-Apim-Subscription-Key': _key_accent, 'Content-Type': 'application/json'}

        json = {'url': picture}
        data = None

        result = process_request(json, data, headers, params, _url_accent)

        dominant_color = result['color']['dominantColorForeground']
        background_color = result['color']['dominantColorBackground']
        accent_color = '#' + result['color']['accentColor']

        if is_hex_color(dominant_color):
            hex_dominant_color = dominant_color
        else:
            hex_dominant_color = webcolors.CSS3_NAMES_TO_HEX[dominant_color.lower()]

        if is_hex_color(background_color):
            hex_background_color = background_color
        else:
            hex_background_color = webcolors.CSS3_NAMES_TO_HEX[background_color.lower()]

        if is_hex_color(accent_color):
            hex_accent_color = accent_color
        else:
            hex_accent_color = webcolors.CSS3_NAMES_TO_HEX[accent_color.lower()]

        r, g, b = hex_to_rgb(hex_dominant_color)
        rgb_dominant_color = '{},{},{}'.format(r, g, b)

        r, g, b = hex_to_rgb(hex_background_color)
        rgb_background_color = '{},{},{}'.format(r, g, b)

        r, g, b = hex_to_rgb(hex_accent_color)
        rgb_accent_color = '{},{},{}'.format(r, g, b)

        cap = Cap.objects.create(name=name,
                                 picture=picture,
                                 url=url,
                                 price=int(float(price) * 100),
                                 emotion=emotion,
                                 hexDominantColor=hex_dominant_color,
                                 hexBackgroundColor=hex_background_color,
                                 hexAccentColor=hex_accent_color,
                                 rgbDominantColor=rgb_dominant_color,
                                 rgbBackgroundColor=rgb_background_color,
                                 rgbAccentColor=rgb_accent_color)

        cap.save()

    return render(request, 'add_cap.html', {'title': 'Add Caps'})


def index(request):
    return render(request, 'index.html', {'title': ''})


def cappr_image(request):
    return render(request, 'cappr_image.html', {'title': 'Upload Image'})


def cappr_view(request):
    imgData = request.POST.get('image')

    with open("media/user.png", "wb") as fh:
        fh.write(imgData.decode('base64'))

    imgur_link = upload_to_imgur(imgData)

    hex_accent_color, current_emotion = get_accent_color_and_emotion(imgur_link)

    r, g, b = hex_to_rgb(hex_accent_color)
    rgb_accent_color = '{},{},{}'.format(r, g, b)

    order = return_top_matches(rgb_accent_color, 2)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(order)])
    caps = Cap.objects.filter(pk__in=order).order_by(preserved)

    cap_list = []
    for cap in caps:

        if current_emotion in cap.emotion:
            cap_list.append(cap)


    get_merged_image()
    return render(request, 'cappr_view.html', {'title': 'Cappr', 'caps': cap_list})


def cappr_redirect(request):
    return redirect('cappr:image')
