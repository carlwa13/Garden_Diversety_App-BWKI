import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
data_dir = "DATA"
# MODELS_DIR wird für das speichen und aufrufen des trainierten Models braucht
MODELS_DIR = os.path.abspath("Programm")
MODELS_FILE_PATH = os.path.join(MODELS_DIR,"model.h5")


batch_size = 8
img_height = 180
img_width = 180

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.1,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.1,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

class_names = train_ds.class_names
print(class_names)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
print(np.min(first_image), np.max(first_image))
num_classes = 5

model = Sequential([
  layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.experimental.preprocessing.RandomFlip("horizontal_and_vertical"),
  layers.experimental.preprocessing.RandomRotation(0.2),
  layers.experimental.preprocessing.RandomTranslation(0.1,0.1),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(80, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(100, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(200, activation='relu'),
  layers.Dense(num_classes)
])

model.compile(optimizer='Adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

epochs=1
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)
model.save_weights(filepath=MODELS_FILE_PATH)

#model.load_weights(filepath=MODELS_FILE_PATH)
#dir_picture = test_picture
#img_array, labels = tf.keras.preprocessing.image_dataset_from_directory(dir_picture, label_mode="int")

#predictions = model.predict(img_array)
#score = tf.nn.softmax(predictions[0])
