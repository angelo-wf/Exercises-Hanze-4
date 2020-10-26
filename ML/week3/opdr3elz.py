
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import random
import tensorflow as tf
from tensorflow import keras

# images are 75*75, 1000 of them
# there are 39 categories

def plot_image(img, lbl):
    plt.imshow(img, cmap="gray")
    plt.title(lbl)
    plt.show()

def plot_matrix(mat, lbl):
    plt.matshow(mat)
    plt.title(lbl)
    plt.show()

def load_images(path):
    # go over each image and load the pixels
    # put these in a np.array with shape (1000, 75, 75), values in range 0 - 1, in random order
    # return it, an np.array with matching categories (1000,) , and a dict from category to name {0: "0.0.normal", etc}
    data = np.zeros((1000, 75, 75))
    labels = np.zeros((1000,))
    labelmap = {}

    counter = 0
    rnd_idx = list(range(1000))
    random.shuffle(rnd_idx)

    dirs = [path + "/" + x for x in os.listdir(path) if os.path.isdir(path + "/" + x)]
    for ind, dir in enumerate(dirs):
        labelmap[ind] = dir.split("/")[-1]
        items = [dir + "/" + x for x in os.listdir(dir) if x[-4:] == ".JPG" or x[-4:] == ".jpg"]
        for image in items:
            imgdata = imageio.imread(image)
            data[rnd_idx[counter],:,:] = imgdata / 255
            labels[rnd_idx[counter]] = ind
            counter += 1

    return data, labels, labelmap

def create_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(256, activation="relu", input_shape=(75*75,)))
    model.add(keras.layers.Dense(39, activation="softmax"))
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model

print("Loading images...")
data, labels, labelmap = load_images("Fundus-data")
print("Loaded images")

data = data.reshape((1000, 75*75))
labels_mat = keras.utils.to_categorical(labels, num_classes=39)

model = create_model()
print("Training...")
model.fit(data, labels_mat, epochs=50)
print("Finished training")

loss, accuracy = model.evaluate(data, labels_mat)
print("Final loss: {}, final accuracy: {}".format(loss, accuracy))

predictions = model.predict(data)
pred_cat = np.argmax(predictions, axis=1)

confusion_mat = tf.math.confusion_matrix(labels, pred_cat)
print("Categories:")
for k, v in labelmap.items():
    print("{}: {}".format(k, v))
plot_matrix(confusion_mat, "Confusion matrix")
