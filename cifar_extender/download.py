import os
import sys
import csv

import numpy as np
import requests
from bs4 import BeautifulSoup
import cv2
import nltk
import torch
from torchvision.utils import save_image


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
        except:
            pass

    np.random.shuffle(image_urls)  # randomize order

    return image_urls


def download_image(data_dir, file_name, url, category=None):
    """
    download image from url to disk

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
        if image.status_code == 200:

            with open(os.path.join(data_dir, file_path), 'wb') as file:
                file.write(image.content)
                # pass
        else:
            print("ERROR {}: {}".format(image.status_code, url))

    except Exception as e:
        print(e)
        pass


def gather_images(search, num_images=None):
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
        print(f" {i+1}/{num_images} - {file}")

        download_image(DATA_DIR, file, url, category=search)


def main(n=25, dataset=CIFAR10):
    for obj in dataset:
        print(obj)
        gather_images(obj, num_images=n)


if __name__ == "__main__":
    try:
        main(n=int(sys.argv[1]))
    except:
        main()
