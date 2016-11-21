import requests
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor, LabColor
from django.conf import settings

from Cappr.models import Cap


def process_request(headers, params, url, json=None, data=None):
    """
    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    result = None

    response = requests.post(url=url, json=json, data=data, headers=headers, params=params)

    if response.status_code == 429:

        print("Message: %s" % (response.json()['error']['message']))

    elif response.status_code == 200 or response.status_code == 201:

        if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
            result = None
        elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
            if 'application/json' in response.headers['content-type'].lower():
                result = response.json() if response.content else None
            elif 'image' in response.headers['content-type'].lower():
                result = response.content
    else:
        print("Error code: %d" % response.status_code)
        print("Message: %s" % (response.json()['error']['message']))

    return result


def get_accent_color(img_data):
    """
    :param img_data: Image Data in Bytes
    :return: Accent Color of the Image
    """
    params = {'visualFeatures': 'Color'}

    headers = {'Ocp-Apim-Subscription-Key': settings.API_KEY_VISION, 'Content-Type': 'application/octet-stream'}

    result = process_request(headers, params, settings.URL_VISION_API, data=img_data)

    accent = '#' + result['color']['accentColor']

    return accent


def get_similarity(accent, dominant):
    """
    :param accent: User's Accent Color
    :param dominant: Cap's Dominant Color
    :return: Similarity between the two.
    """

    accent_red, accent_green, accent_blue = map(float, accent.split(','))

    accent_rgb = sRGBColor(accent_red, accent_green, accent_blue)
    accent_lab = convert_color(accent_rgb, LabColor)

    dom_red, dom_green, dom_blue = map(float, dominant.split(','))

    dom_rgb = sRGBColor(dom_red, dom_green, dom_blue)
    dom_lab = convert_color(dom_rgb, LabColor)

    delta_e = delta_e_cie2000(accent_lab, dom_lab)

    return delta_e


def get_matches(accent, n):
    """
    :param accent: User's Accent Color
    :param n: The number of results to return
    :return: List of Cap matches sorted by Similarity
    """

    similarity_values = []
    caps = Cap.objects.all()
    for cap in caps:
        rgb = cap.rgb
        dominant = rgb.dominant
        similarity_values.append((cap.SKU, get_similarity(accent, dominant)))

    similarity_values.sort(key=lambda tup: tup[1])

    return [x[0] for x in similarity_values[:n]]
