# -*- coding: utf-8 -*-
"""ImageFeatures.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/100a35NdGzMqDiMt6Z1h3NMGGnXwHQxb9
"""

# Commented out IPython magic to ensure Python compatibility.
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os

# %matplotlib inline

image = cv2.imread('/content/drive/MyDrive/Dress/dressimage.jpg')
print("The type of this input is {}".format(type(image)))
print("Shape: {}".format(image.shape))
plt.imshow(image)

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image)

# function that will convert RGB to hex so that we can use them as labels for our pie chart

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

#get an image into Python in the RGB space
def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_colors(image, number_of_colors, show_chart):
    
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    
    counts = Counter(labels)
    # sort to ensure correct color percentage
    counts = dict(sorted(counts.items()))
    
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
    
    return rgb_colors

get_colors(get_image('/content/drive/MyDrive/Dress/dressimage.jpg'),15, True)

import numpy as np
import pandas as pd
import os
import cv2
from sklearn.metrics import classification_report
import seaborn as sn; sn.set(font_scale=1.4)
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import tensorflow as tf
from tqdm import tqdm

cloth_data = pd.read_csv("/content/drive/MyDrive/Dress/Myntra_Women_Clothing_Dataset.csv")
cloth_data.drop(['Item_Url', 'Native_Product_Id', 'Primary_Colour'], inplace=True, axis=1)

print(cloth_data)

#take first 70015 from the dataset
cloth_data = cloth_data.iloc[:70015]

print(len(cloth_data))
print(cloth_data)

cloth_data.isnull().sum()

cloth_data = cloth_data.dropna()
print(len(cloth_data))

cloth_data.isnull().sum()

cloth_data['Pattern'].unique()

cloth_data['Print'].unique()

cloth_data['Fabric'].unique()

from sklearn import preprocessing

label_encoder = preprocessing.LabelEncoder()

cloth_data['Pattern']= label_encoder.fit_transform(cloth_data['Pattern'])
cloth_data['Print']= label_encoder.fit_transform(cloth_data['Print'])
cloth_data['Fabric']= label_encoder.fit_transform(cloth_data['Fabric'])

cloth_data['Pattern'].unique()

cloth_data['Print'].unique()

cloth_data['Fabric'].unique()

print(cloth_data.head)

columns = ['Pattern', 'Print', 'Fabric']
cloth_data["allData"] = cloth_data[columns].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

print(cloth_data.head)

print(cloth_data['allData'][0])

def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False


class_names = []
for i in range(90000):
  try:
    loopClass = cloth_data['allData'][i]
  except:
    continue

  loopClass = cloth_data['allData'][i]

  if search(class_names, loopClass):
    continue
  else:
    class_names.append(loopClass)

print(class_names)
print(len(class_names))

class_names_label = {class_name:i for i, class_name in enumerate(class_names)}

nb_classes = len(class_names)

print(class_names_label)

IMAGE_SIZE = (150,150)

!mkdir /content/data
!mkdir /content/data/seg_train
!mkdir /content/data/seg_test

for i in range(nb_classes):
  
  os.mkdir('/content/data/seg_train/'+class_names[i])
  os.mkdir('/content/data/seg_test/'+class_names[i])

hi = cloth_data['allData'].value_counts()["19_36_59"]
print(hi)
num = round((hi*20)/100)

df = cloth_data.loc[cloth_data['allData'] == "0_0_2"]
listof = df.iat[0,3]
#print(df.iloc[0:1].values)
print(listof)

def Convert(string):
    li = list(string.split("'"))
    li = list(filter(("[").__ne__, li))
    li = list(filter((", ").__ne__, li))
    li = list(filter(("]").__ne__, li))
    return li
  
# Driver code    
str1 = listof
str1 = Convert(str1)
os.path.join("/content/data/seg_train/0_0_2/", str1[0])
print(str1)

print(df)

def Convert(string):
    li = list(string.split("'"))
    li = list(filter(("[").__ne__, li))
    li = list(filter((", ").__ne__, li))
    li = list(filter(("]").__ne__, li))
    return li



def split_each_class(nameOfClass):

  frameOfSection = cloth_data.loc[cloth_data['allData'] == nameOfClass]
  cntTrain = 0
  cntTest = 0
  LenInColumn = cloth_data['allData'].value_counts()[nameOfClass]
  split = round((LenInColumn*20)/100)
  #print(frameOfSection, LenInColumn)
  for j in range(LenInColumn):
    #print(df.iat[j,3])
    getImages = df.iat[j,3]
    getImages = Convert(getImages)

    if cntTrain < LenInColumn-split:
      for img in range(len(getImages)):
        os.path.join("/content/data/seg_train/", str(nameOfClass), getImages[img])
      cntTrain+=1
    
    else:
      for img in range(len(getImages)):
        os.path.join("/content/data/seg_test/", str(nameOfClass), getImages[img])
      cntTest+=1

  


for i in range(nb_classes):

  name = class_names[i]

  split_each_class(name)

def load_data():
  dir = r"/content/data"
  CATEGORY = ["seg_train","seg_test"]

  output = []

  for category in CATEGORY:
    path = os.path.join(dir, category)
    images = []
    labels = []

    for folder in os.listdir(path):
      label = class_names_label[folder]

      for file in os.listdir(os.path.join(folder, folder)):

        img_path = os.path.join(os.path.join(path, folder), file)

        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, IMAGE_SIZE)

        images.append(image)
        labels.append(label)

    images = np.array(images, dtype = 'float32')
    labels = np.array(labels, dtype = 'int32')

  return output

(train_images, train_labels), (test_images, test_labels) = load_data()
train_images, train_labels = shuffle(train_images, train_labels, random_state=25)

import keras,os
from keras.models import Model
from keras.layers import Dense, Conv2D, MaxPooling2D , Flatten, Input
from keras.preprocessing.image import image
import numpy as np
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16

model = VGG16(weights='imagenet', include_top=False)
model = Model(inputs = model.inputs, outputs = model.layers[-5].output)

train_features = model.predict(train_images)
test_features = model.predict(test_images)

model2 = VGG16(weights='imagenet', include_top=False)

input_shape = model2.layers[-4].get_input_shape_at(0)
layer_input = Input(shape = (9,9,512))

x = layer_input
for layer in model2.layers[-4::1]:
  x = layer(x)

x = Conv2D(64, (3,3), activation='relu')(x)
x = MaxPooling2D(pool_size=(2,2))(x)
x= Flatten()(x)
x = Dense(100, activation='relu')(x)
x = Dense(6, activation='softmax')(x)


new_model = Model(layer_input, x)

new_model.compile(optimizer='adam', loss = 'sparse_categorical_crossentropy', metrics=['accuracy'])

history = new_model.fit(train_features, train_labels, batch_size =128, epochs = 10, validation_split = 0.2)

plot_accuracy_loss(history)