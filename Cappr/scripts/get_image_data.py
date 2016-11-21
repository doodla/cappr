import webcolors
from django.conf import settings

from Cappr.lib.utils import process_request
from Cappr.models import Cap, RGB, HEX


def run():
    count = 0
    caps = Cap.objects.all()

    for cap in caps:

        count += 1

        print(count)

        rgb = cap.rgb

        img_url = cap.image_url('COVER', 'LEFT')

        if rgb is None:
            _json = {'url': img_url}
            params = {'visualFeatures': 'Color'}
            headers = {'Ocp-Apim-Subscription-Key': settings.API_KEY_VISION, 'Content-Type': 'application/json'}

            result = process_request(headers, params, json=_json)

            dominant_color = result['color']['dominantColorForeground']
            background_color = result['color']['dominantColorBackground']
            accent_color = '#' + result['color']['accentColor']

            try:
                dominant_color = webcolors.normalize_hex(dominant_color)
            except ValueError:
                dominant_color = webcolors.CSS3_NAMES_TO_HEX[dominant_color.lower()]

            try:
                background_color = webcolors.normalize_hex(background_color)
            except ValueError:
                background_color = webcolors.CSS3_NAMES_TO_HEX[background_color.lower()]

            hex = HEX.objects.create(
                dominant=dominant_color,
                background=background_color,
                accent=accent_color
            )

            r, g, b = webcolors.hex_to_rgb(dominant_color)
            dominant_color = '{},{},{}'.format(r, g, b)

            r, g, b = webcolors.hex_to_rgb(background_color)
            background_color = '{},{},{}'.format(r, g, b)

            r, g, b = webcolors.hex_to_rgb(accent_color)
            accent_color = '{},{},{}'.format(r, g, b)

            rgb = RGB.objects.create(
                dominant=dominant_color,
                background=background_color,
                accent=accent_color
            )
            cap.hex = hex
            cap.rgb = rgb

            cap.save()
