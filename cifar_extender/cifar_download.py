#!/usr/bin/env python3
import os
import sys
import csv
import asyncio

import numpy as np
import requests
from bs4 import BeautifulSoup
import nltk


DATA_DIR = 'images/'  # where the images will be stored
CIFAR10 = ['airplane', 'car', 'bird', 'cat', 'deer',  # automobile to car
           'dog', 'frog', 'horse', 'ship', 'truck']


def get_image_urls(search_item):
    """
    return image urls from https://www.image-net.org

    :param search_item: WNID to search for
    :type search_item: str
    """
    print("Getting {} image urls...".format(search_item))
    # search for images by wnid
    url = "http://www.image-net.org/search?q={}".format(search_item)
    html = requests.get(url, timeout=5)  # url connect
    soup = BeautifulSoup(html.text, 'lxml')  # create soup object
    tags = []
    # find table
    for search in soup.findAll(name='table', attrs={'class', 'search_result'}):
        for a in search.findAll(name='a'):  # find href tag
            try:  #prevent breaking
                tags.append(a['href'].split('?')[1])  # href w/ wnid link
                break  # only get first wnid
            except IndexError:
                pass

    image_urls = []

    print("TAGS: ", tags)

    for tag in tags:
        # image net search id
        url = "http://www.image-net.org/api/text/imagenet.synset.geturls?{}".format(tag)
        try:
            print("URL:", url)
            html = requests.get(url)  # html for search
            urls = (image_url for image_url in html.text.split('\r\n'))
            image_urls = [url for url in urls if url != '\n']
            # TODO(@messiest) Break parsing and downloading into two modules
        except:
            pass

    np.random.shuffle(image_urls)  # randomize order

    return image_urls


def download_image(loop, data_dir, file_name, url, category=None):
    """
    download image from url to disk

    :param loop: event loop for the downloading.
    :type loop: asyncio.AbstractEventLoop()
    :param data_dir: key for the image file, used as the file name
    :type data_dir: str
    :param file_name: name for the image file, used as the file name
    :type file_name: str
    :param url: url to the image file
    :type url: str
    :param category: categeory for the image, used to save to a class directory
    :type category: str
    :return: None
    :rtype: None
    """
    file_path = os.path.join(category, file_name)
    try:
        image = requests.get(url, allow_redirects=False, timeout=5)
    except Exception as e:
        print(e)
        return e

    headers = image.headers

    if image.status_code != 200:
        print("CONNECTION ERROR {}: {}".format(image.status_code, url))
    elif headers['Content-Type'] != 'image/jpeg':
        print("FILE TYPE ERROR {}: {}".format(headers['Content-Type'], url))
    elif int(headers['Content-Length']) < 50000:
        print("FILE SIZE ERROR {}: {}".format(headers['Content-Length'], url))
    else:
        with open(os.path.join(data_dir, file_path), 'wb') as file:
            file.write(image.content)  #

    loop.stop()


def gather_images(loop, search, num_images=None):
    """
    search for images on ImageNet, write images to disk

    :param search: term to search ImageNet for
    :type search: str
    :param num_images: total number of images to download
    :type num_images: int
    """

    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    if isinstance(search, nltk.corpus.reader.wordnet.Synset):
        # get object name from synset
        search = search.name().split('.')[0].replace('_', ' ')

    print("\nSearching for {} images...".format(search))
    # url format for search url
    search_url = search.replace(' ', '+').replace(',', '%2C').replace("'", "%27")
    # file format for file system
    search = search.replace(', ', '-').replace(' ', '_').replace("'", "")

    if not os.path.exists(DATA_DIR + search):
        os.mkdir(DATA_DIR + search)

    # get list of image urls
    image_urls = [url for url in get_image_urls(search_url)]
    total_urls = len(image_urls)  # number of total urls
    print("  {} image urls found".format(total_urls))
    for i, url in enumerate(image_urls):  # start with last used url
        if i == num_images:  # only download set number of images
            break
        file = url.split('/')[-1]  # image file name
        if os.path.splitext(file)[1] != ".jpg":  # skip non jpg files
            continue
        loop.call_soon(download_image, loop, DATA_DIR, file, url, search)
        # download_image(DATA_DIR, file, url, category=search)

    # print(f" {i+1}/{num_images} - {file}")


def main(n=100, dataset=CIFAR10):
    if len(sys.argv) > 1:  # catch sys args
        n = int(sys.argv[1])
    # if len(sys.argv) > 2:  # look into optparse / argparse / click
    loop = asyncio.get_event_loop()  # async event loop
    for obj in dataset:
        gather_images(loop, obj, num_images=n)
    #TODO (@messiest) figure out the looping, re making sure there are 100 images
    loop.run_forever()  # execute queued work
    loop.close()  # shutdown loop


if __name__ == "__main__":
    main()
