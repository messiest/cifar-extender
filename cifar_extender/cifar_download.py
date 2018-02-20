#!/usr/bin/env python3.6
import os
import csv
import asyncio
from collections import defaultdict

import requests


IMG_DIR = "./images/"


def download_image(loop, image_dir, url, category):
    """
    download image from url to disk

    :param loop: event loop for the downloading.
    :type loop: asyncio.AbstractEventLoop()
    :param image_dir: key for the image file, used as the file name
    :type image_dir: str
    :param url: url to the image file
    :type url: str
    :param category: categeory for the image, used to save to a class directory
    :type category: str
    :return: None
    :rtype: None
    """
    file_name = url.split('/')[-1]
    file_path = os.path.join(category, file_name)

    try:
        image = requests.get(url, allow_redirects=False, timeout=5)
    except Exception as e:
        print(e)
        return e

    headers = image.headers

    if image.status_code != 200:
        print("\tCONNECTION ERROR {}: {}".format(image.status_code, url))
    elif headers['Content-Type'] != 'image/jpeg':
        print("\tFILE TYPE ERROR {}: {}".format(headers['Content-Type'], url))
    elif int(headers['Content-Length']) < 50000:  # only files > 50kb
        print("\tFILE SIZE ERROR {}: {}".format(headers['Content-Length'], url))
    else:
        with open(os.path.join(image_dir, file_path), 'wb') as file:
            file.write(image.content)  # download image

    loop.stop()  # escape loop iteration


def get_collection(filename):
    collection = defaultdict(list)
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            category, url = row
            collection[category].append(url)

    return collection


def main(datafile):
    d = get_collection(datafile)
    loop = asyncio.get_event_loop()  # async event loop
    for k in d.keys():
        for url in d[k]:
            loop.call_soon(download_image, loop, IMG_DIR, url, k)

    loop.run_forever()  # execute queued work
    loop.close()  # shutdown loop


if __name__ == "__main__":
    main('data/images.csv')
