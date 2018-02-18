"""
download images from image-net.org to s3 bucket
"""
import os
import numpy as np

from imagenet import search
from s3.bucket import S3Bucket


IMG_DIR = 'images/'
BUCKET = 'cifar-extended'
CIFAR10 = ['airplane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']  # automobile changed to car


def create_image_key(url, obj):
    file_name = url.split('/')[-1]
    key = f"{IMG_DIR}/{obj}/{file_name}"

    return key


def main():
    bucket = S3Bucket(BUCKET)  # TODO (@messiest) remove the auto-run for get_keys()/get_objects()
    for obj in CIFAR10:
        urls = [j for j in search.get_image_urls(obj) if os.path.splitext(j)[1] in ['.jpg', '.jpeg']]
        np.random.shuffle(urls)  # randomize order

        for img_url in urls:
            key = create_image_key(img_url, obj)
            bucket.download_image(key, url=img_url, tag=obj)


if __name__ == "__main__":
    print("Running Downloader...")
    main()
    bucket = S3Bucket(BUCKET)
    keys = bucket.get_keys()
    for k in keys:
        print(k)
