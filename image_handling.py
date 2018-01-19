"""
currently not working due to a lack of image data...
"""
import os
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt


IMG_DIR = '/repos/doodle-bot-learn/assets/images/'


def get_image_files():
    files = {obj: os.listdir(f'{IMG_DIR}/{obj}/') for obj in os.listdir(f'{IMG_DIR}/')}
    hold = []
    for label in files.keys():
        for file in files[label]:
            hold.append(f'{IMG_DIR}/{label}/{file}')

    return hold


def build_trainer(files, resize=False):
    filename_queue = tf.train.string_input_producer(files)  # queue for the file names

    file_reader = tf.WholeFileReader()  # file reader object for image files
    key, value = file_reader.read(filename_queue)  # read the files

    # TODO(@messiest) understand difference b/w decode_jpeg and decode_image
    img = tf.image.decode_jpeg(value, channels=3)  # decode image file
    img = tf.image.convert_image_dtype(img, tf.float32)  # cast to tf.float32

    if resize:
        img = tf.image.resize_images(img, [128, 128])  # resize the image

    print(type(img))

    return img


def run(images):
    with tf.Session() as sess:
        coord = tf.train.Coordinator()  # instantiate the training coordinator
        threads = tf.train.start_queue_runners(coord=coord) # populate the filename queue

        file_names = get_image_files()

        print(file_names)

        for i, _ in enumerate(file_names):  # iterate over files
            image = sess.run(images)
            if i % 100 == 0:  # display every 100th image
                plt.imshow(image)  # display image
    #             plt.axis('off')
                plt.show()  # display each image
                print("Dimensions: ", image.shape)  # output image array shape

        coord.request_stop()
        coord.join(threads)


def main():
    file_names = get_image_files()
    print(file_names)
    np.random.shuffle(file_names)  # randomize order
    images = build_trainer(file_names, resize=False)

    print(images)
    run(images)


if __name__ == "__main__":
    print("Program start.")
    main()
