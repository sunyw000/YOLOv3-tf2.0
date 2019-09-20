#!/usr/bin/python3

import tensorflow as tf;
import tensorflow_datasets as tfds;
from YOLOv3 import YOLOv3, Loss;
from preprocess import map_function;

batch_size = 8;

def main():
    
    # yolov3 model
    yolov3 = tf.keras.models.load_model('yolov3.h5', compile = False);
    yolov3_loss = Loss((416,416,3), 80);
    # load downloaded dataset
    testset = tfds.load(name = "coco2014", split = tfds.Split.TEST, download = False);
    testset = testset.map(map_function).repeat(100).shuffle(batch_size).batch(batch_size).prefetch(tf.data.experimental.AUTOTUNE);
    avg_loss = tf.keras.metrics.Mean(name = 'loss', dtype = tf.float32);
    count = 0;
    for images,labels in testset:
        outputs = yolov3(images);
        loss = yolov3_loss([*outputs, *labels]);
        avg_loss.update_state(loss);
        print('Step #%d Loss: %.6f' % (count, loss));
        if tf.equal(count % 10, 0):
            avg_loss.reset_states();
        count += 1;

if __name__ == "__main__":

    assert tf.executing_eagerly();
    main();