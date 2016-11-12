import json
import operator
import time

import requests
import webcolors
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor, LabColor

from CapFinder.models import Cap

_maxNumRetries = 10
_key_accent = '00ddd41708ea42b2b6afdc73b574d2d7'
_url_accent = 'https://api.projectoxford.ai/vision/v1/analyses'
_url_emotion = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key_emotion = '36c531a3defc46c38518eec7da08488e'


def process_request(json, data, headers, params, _url):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request('post', _url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:

            print("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

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

        break

    return result


def is_hex_color(color):
    try:
        color = webcolors.normalize_hex(color.lower())
        return True
    except ValueError:
        return False


def upload_to_imgur(imgData):
    headers = {"Authorization": "Client-ID 4d6957ec71171dd"}

    _imgur_client = '4d6957ec71171dd'

    url = "https://api.imgur.com/3/upload"

    j1 = requests.post(
        url,
        headers=headers,
        data={
            'key': _imgur_client,
            'image': imgData,
            'type': 'base64',
            'name': 'photo.jpg',
            'title': 'Photo'
        }
    )

    data = json.loads(j1.text)['data']
    return data['link']


def get_accent_color_and_emotion(imgur_link):
    params = {'visualFeatures': 'Color,Categories'}

    headers = {'Ocp-Apim-Subscription-Key': _key_accent, 'Content-Type': 'application/json'}

    json = {'url': imgur_link}
    data = None

    result = process_request(json, data, headers, params, _url_accent)

    hex_accent_color = '#' + result['color']['accentColor']

    headers['Ocp-Apim-Subscription-Key'] = _key_emotion

    result = process_request(json, data, headers, params, _url_emotion)

    for currFace in result:
        current_emotion = max(currFace['scores'].items(), key=operator.itemgetter(1))[0]
        return hex_accent_color, current_emotion


def get_similarity(accent, dominant):
    accent_red, accent_green, accent_blue = map(float, accent.split(','))

    accent_rgb = sRGBColor(accent_red, accent_green, accent_blue)
    accent_lab = convert_color(accent_rgb, LabColor)

    dom_red, dom_green, dom_blue = map(float, dominant.split(','))

    dom_rgb = sRGBColor(dom_red, dom_green, dom_blue)
    dom_lab = convert_color(dom_rgb, LabColor)

    delta_e = delta_e_cie2000(accent_lab, dom_lab)

    return delta_e


def return_top_matches(rgb_accent_color, n):
    similarity_values = []

    caps = Cap.objects.all()
    for cap in caps:
        rgb_dominant_color = cap.rgbDominantColor

        similarity_values.append((cap.id, get_similarity(rgb_accent_color, rgb_dominant_color)))

    similarity_values.sort(key=lambda tup: tup[1])

    return [x[0] for x in similarity_values]
