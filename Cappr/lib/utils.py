import requests
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor, LabColor

from Cappr.models import Cap

_maxNumRetries = 10
_key_accent = '00ddd41708ea42b2b6afdc73b574d2d7'
_url_accent = 'https://api.projectoxford.ai/vision/v1/analyses'
_url_emotion = 'https://api.projectoxford.ai/emotion/v1.0/recognize'


def process_request(headers, params, _url, _json=None, data=None):
    """
    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    result = None

    response = requests.post(_url, json=_json, data=data, headers=headers, params=params)

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
    params = {'visualFeatures': 'Color,Categories'}

    headers = {'Ocp-Apim-Subscription-Key': _key_accent, 'Content-Type': 'application/octet-stream'}

    result = process_request(headers, params, _url_accent, data=img_data)

    hex_accent_color = '#' + result['color']['accentColor']

    return hex_accent_color


def get_similarity(accent, dominant):
    accent_red, accent_green, accent_blue = map(float, accent.split(','))

    accent_rgb = sRGBColor(accent_red, accent_green, accent_blue)
    accent_lab = convert_color(accent_rgb, LabColor)

    dom_red, dom_green, dom_blue = map(float, dominant.split(','))

    dom_rgb = sRGBColor(dom_red, dom_green, dom_blue)
    dom_lab = convert_color(dom_rgb, LabColor)

    delta_e = delta_e_cie2000(accent_lab, dom_lab)

    return delta_e


def get_matches(rgb_accent_color):
    similarity_values = []

    caps = Cap.objects.all()
    for cap in caps:
        rgb_dominant_color = cap.rgbDominantColor

        similarity_values.append((cap.id, get_similarity(rgb_accent_color, rgb_dominant_color)))

    similarity_values.sort(key=lambda tup: tup[1])

    return [x[0] for x in similarity_values]
