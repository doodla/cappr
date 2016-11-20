from __future__ import print_function

import math

from PIL import Image

from .utils import process_request

url = 'https://api.projectoxford.ai/face/v1.0/detect'
_key = '88116df7de534533b893886ac1120b26'


user_image_path = 'media/user/'
path_to_cap = 'media/cap.png'
resize_path = 'media/resize.png'
rotate_path = 'media/rotate.png'
merged_path = 'media/merged.png'


def get_angle(x_orig, y_orig, x_landmark, y_landmark):
    delta_y = y_landmark - y_orig
    delta_x = x_landmark - x_orig
    return math.atan2(delta_y, delta_x) * 180 / math.pi


def find_middle_point(x, y, a, b):
    return x - (x - a) / 2, y - (y - b / 2)


def change_cap_width(width):
    im = Image.open(path_to_cap)

    old_width, old_height = im.size

    ratio = float(width) / float(old_width)

    ratio *= 1.7

    new_width, new_height = int(old_width * ratio), int(old_height * ratio)

    im.thumbnail((new_width, new_height), Image.LANCZOS)

    im.save(resize_path)


def rotate_cap(angle):
    im = Image.open(resize_path)
    im.rotate(angle)
    im.save(rotate_path)


def place_image(mx, my):
    background = Image.open(user_image_path)
    cap = Image.open(rotate_path)
    w, h = cap.size
    background.paste(cap, (int(mx - w / 2), int(my - h / 2)), cap)
    background.save(merged_path)


def get_merged_image(img_data):
    params = {'returnFaceAttributes': 'age,gender',
              'returnFaceLandmarks': 'true'}

    headers = {'Ocp-Apim-Subscription-Key': _key, 'Content-Type': 'application/octet-stream'}

    result = process_request(headers, params, url, data=img_data)

    coordinates = []
    faces_width = []
    face_rectangle_coords = []

    for i in result:
        coordinates.append((i['faceLandmarks']['eyebrowLeftOuter'], i['faceLandmarks']['eyebrowRightOuter']))
        faces_width.append(i['faceRectangle']['width'])
        face_rectangle_coords.append((i['faceRectangle']['top'], i['faceRectangle']['left']))

    change_cap_width(faces_width[0])

    mx, my = find_middle_point(coordinates[0][0]['x'], coordinates[0][0]['y'], coordinates[0][1]['x'],
                               coordinates[0][1]['y'])

    angle = 0
    # print (coordinates)
    for cord in coordinates:
        angle = get_angle(cord[0]['x'], cord[0]['y'], cord[1]['x'], cord[1]['y'])

    rotate_cap(angle)

    place_image(mx, my)
