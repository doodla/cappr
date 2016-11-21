import os.path
from io import BytesIO

import requests
from PIL import Image

from Cappr.models import Cap


def run():
    caps = Cap.objects.all()

    count = 0

    for cap in caps:

        count += 1
        img_url = cap.image_url('HIGH-RES', 'CENTER')
        print(count)
        SKU = cap.SKU
        file_name = SKU + '.png'

        if not os.path.isfile('media/pngs/' + file_name):

            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))

            img = img.convert("RGBA")
            datas = img.getdata()

            newData = []
            for item in datas:
                if item[0] > 249 and item[1] > 249 and item[2] > 249:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)

            img.putdata(newData)
            img.save('media/pngs/' + file_name, "PNG")

            # image = Image.open('media/pngs/' + SKU + '.png')
            # image.convert("RGBA")  # Convert this to RGBA if possible
            #
            # canvas = Image.new('RGBA', image.size, (255, 255, 255, 255))  # Empty canvas colour (r,g,b,a)
            # canvas.paste(image, mask=image)  # Paste the image onto the canvas, using it's alpha channel as mask
            # canvas.save('media/pngs/' + SKU + '.png', format="PNG")
