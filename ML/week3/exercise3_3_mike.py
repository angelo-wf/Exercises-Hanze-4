from os import listdir
from os.path import isdir, isfile, join
from math import floor

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf
from tensorflow import keras  

def getPath():
    return "./Exercises-Hanze-4/ML/week3/Fundus-data"

def getDirs():
    path = getPath()
    dirs = [d for d in listdir(path) if isdir(join(path, d))]
    return dirs

def getData():
    path = getPath()
    dirs = getDirs()
    train_images = []
    train_labels = []
    test_images = []
    test_labels = []
    data = (train_images, train_labels, test_images, test_labels)
    label_index = 0
    for dir in dirs:
        file_paths = [join(path, dir, f) for f in listdir(join(path, dir)) if isfile(join(path, dir, f))]
        amout_of_train_images = floor(len(file_paths) * 1)
        for i in range(len(file_paths)):
            img = mpimg.imread(file_paths[i])
            # if i < amout_of_train_images:
            #     train_images.append(img)
            #     train_labels.append(label_index)
            # else: 
            #     test_images.append(img)
            #     test_labels.append(label_index)
            train_images.append(img)
            train_labels.append(label_index) 
            test_images.append(img)
            test_labels.append(label_index)
        label_index += 1
    data = [np.array(l) for l in data]
    return data

def plotImage(img, label):
    plt.imshow(img, cmap='gray')
    plt.title(label)
    plt.show()

def plotMatrix(data):
    plt.matshow(data)
    plt.show()

def scaleData(X):
    max_value = np.amax(X)
    return X.astype('float32') / max_value


def buildModel():
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(256, activation='relu', input_shape=(75*75,)))
    model.add(keras.layers.Dense(39, activation='softmax'))

    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    return model

def confMatrix(labels, pred):
    return tf.math.confusion_matrix(labels, pred)

def confEls(conf, labels):
    tp = np.diagonal(conf)
    fp = np.sum(conf, axis=1) - tp
    fn = np.sum(conf, axis=0) - tp
    tn = - tp - fp - fn + np.sum(conf)
    return list(zip(labels, tp, fp, fn, tn))

def confData(metrics):
    metrics = list(zip(*metrics))

    tp = sum(metrics[1])
    fp = sum(metrics[2])
    fn = sum(metrics[3])
    tn = sum(metrics[4])

    tpr = tp / (tp + fn)
    ppv = tp / (tp + fp)
    tnr = tn / (tn + fp)
    fpr = fp / (fp + tn)

    rv = {'tpr':tpr,'ppv':ppv, 'tnr':tnr, 'fpr':fpr }
    return rv

print("Getting Data...")
labels = getDirs()
train_images, train_labels, test_images, test_labels = getData()

print ("Shape of train_images: {}".format(train_images.shape))
print ("Shape of train_labels: {}".format(train_labels.shape))
print ("Shape of test_images: {}".format(test_images.shape))
print ("Shape of test_labels: {}".format(test_labels.shape))
print ("Size of labels: {}".format(len(labels)))

print("Preparing Data...")
train_images = scaleData(train_images)
test_images = scaleData(test_images)

train_images = train_images.reshape((train_images.shape[0], 75*75))
test_images = test_images.reshape((test_images.shape[0], 75*75))
train_labels_cat = keras.utils.to_categorical(train_labels, num_classes=39)
test_labels_cat = keras.utils.to_categorical(test_labels, num_classes=39)

print("Building Model...")
model = buildModel() 

print("Training...")
model.fit(train_images, train_labels_cat, epochs=256)
print("Finished Training!")

print("Preparing Confusing Matrix...")
pred = np.argmax(model.predict(test_images), axis=1)
cm = confMatrix(test_labels, pred)

print("Printing Metrics...")
metrics = confEls(cm, labels)
for t in metrics:
    print("Label {0} heeft TP: {1}, TN: {2}, FP: {3}, FN: {4}".format(*t))

print("Printing Scores ...")
scores = confData(metrics)

print(scores)

print("Scores zijn TPR: {0}, PPV: {1}, TNR: {2}, FPR: {3}".format(*scores.values()))

print("Plotting Confusing Matrix...")
plotMatrix(cm)