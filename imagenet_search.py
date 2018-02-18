from uuid import uuid4

import requests
from bs4 import BeautifulSoup
import numpy as np
import os
import cv2
import nltk
import torch
from torchvision.utils import save_image

from scipy.misc import imsave


IMG_DIR = 'images'
DATA_DIR = 'images/'
BUCKET = 'cifar-extended'
CIFAR10 = ['airplane', 'car', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck']  # automobile changed to car


def get_image_urls(search_item):
    """
    return image urls from https://www.image-net.org

    :param search_item: WNID to search for
    :type search_item: str
    """

    print("Getting {} image urls...".format(search_item))
    url = "http://www.image-net.org/search?q={}".format(search_item)                    # search image by wnid
    html = requests.get(url)                                                            # url connect
    soup = BeautifulSoup(html.text, 'lxml')                                             # create soup object
    tags = []
    for search in soup.findAll(name='table', attrs={'class', 'search_result'}):         # find table
        for a in search.findAll(name='a'):                                              # find href tag
            try:                                                                        # prevent breaking
                tags.append(a['href'].split('?')[1])                                    # href w/ wnid link
                break                                                                   # only get first wnid
            except IndexError:
                pass

    image_urls = []

    print("TAGS: ", tags)

    for tag in tags:
        url = "http://www.image-net.org/api/text/imagenet.synset.geturls?{}".format(tag)  # image net search id
        try:
            print("URL:", url)
            html = requests.get(url)                                                      # html for search
            urls = (image_url for image_url in html.text.split('\r\n'))
            image_urls = [url for url in urls if url != '\n']
        except:
            pass

    return image_urls


def download_image(data_dir, name, url, category=None):
    """
    download images to disk from url

    :param data_dir: key for the image file, used as the file name
    :type data_dir: str
    :param key: key for the image file, used as the file name
    :type key: str
    :param url: url to the image file
    :type url: str
    :param category: categeory for the image, used to save to a class directory
    :type category: str
    :return: None
    :rtype: None
    """

    file_type = url.split('.')[-1]
    filename = "{}/{}.{}".format(category, name, file_type) if category else "{}.{}".format(key, file_type)
    image = requests.get(url)
    if image.status_code == 200:
        with open(data_dir + filename, 'wb') as file:
            file.write(image.content)
    else:
        print("ERROR {}: {}".format(image.status_code, url))


def download_images(search, num_images=None):
    """
    search for images on ImageNet, write images to s3

    :param search: term to search ImageNet for
    :type search: str
    :param num_images: total number of images to download
    :type num_images: int
    """
    if isinstance(search, nltk.corpus.reader.wordnet.Synset):
        search = search.name().split('.')[0].replace('_', ' ')  # get object name from synset

    print("\nSearching for {} images...".format(search))
    search_url = search.replace(' ', '+').replace(',', '%2C').replace("'", "%27")  # formatted for search url
    search = search.replace(', ', '-').replace(' ', '_').replace("'", "")  # formatted for file system

    image_urls = [url for url in get_image_urls(search_url)]  # get list of image urls
    total_urls = len(image_urls)  # number of total urls
    print("  {} image urls found".format(total_urls))

    for i, url in enumerate(image_urls):  # start with last used url
        if i == num_images:  # only download ima
            break
        file = url.split('/')[-1]  # image file name
        if file.split('.')[-1] != "jpg":  # skip non jpg
            continue
        print(f" {i+1}/{total_urls} - {file}")

        key = "images/{}/{}".format(search, file)  # path for image file

        download_image(DATA_DIR, file, url, category=search)


def image_search(search_terms, images=1000):
    """
    perform image search for provided list of WNIDs

    :param search_terms: search terms
    :type search_terms: list
    :param images: number of images to download
    :type images: int
    """
    for search in search_terms:                                                         # iterate over searches
        if search not in os.listdir("images/") or len(os.listdir("images/")) < images:  # ignore populated categories
            download_images(search, num_images=images)                                       # get the images
            pass


def main():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    for obj in CIFAR10:


        download_images(obj, num_images=25)


if __name__ == "__main__":
    main()

