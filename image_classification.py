import numpy as np
import os
import PIL
import io

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from keras.preprocessing import image

def pil_to_numpy(image):
    return np.asarray(image)

def numpy_to_bytes(num):
    return num.tobytes()
  
class Classifier():
    def __init__(self, model_path):
        self.model_path = model_path
        self.batch_size = 32
        self.img_height = 180
        self.img_width = 180
        self.class_names = ['gurke', 'zucchini', 'zuckererbse', 'tomate']
        self.num_classes = 5
        self.model = None

    def load(self):
        self.model = Sequential([
          layers.experimental.preprocessing.Rescaling(1./255, input_shape=(self.img_height, self.img_width, 3)),
          layers.Conv2D(64, 3, padding='same', activation='relu'),
          layers.MaxPooling2D(),
          layers.Conv2D(80, 3, padding='same', activation='relu'),
          layers.MaxPooling2D(),
          layers.Conv2D(100, 3, padding='same', activation='relu'),
          layers.MaxPooling2D(),
          layers.Flatten(),
          layers.Dense(200, activation='relu'),
          layers.Dense(self.num_classes)
        ])

        self.model.load_weights(filepath=self.model_path)

    def predict(self, image_name, image_path):
        #im = PIL.Image.open(image_path)
        #im = pil_to_numpy(im)
        #im = numpy_to_bytes(im)
        #print(im)
        #image = tf.keras.utils.get_file(image_name, origin=image_path)

        
        img = keras.preprocessing.image.load_img(
         image_path, target_size=(self.img_height, self.img_width)
        )

        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) 

        prediction = self.model.predict(img_array)
        score = tf.nn.softmax(prediction[0])

      
        print(prediction)

        return self.class_names[np.argmax(score)-1]
