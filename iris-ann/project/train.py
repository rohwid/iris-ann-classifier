import os
import joblib
import yaml

import numpy as np
import pandas as pd

from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.models import Sequential 
from keras.layers import Dense, Dropout 


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

f = open("params/train.yml", "r")
params = yaml.load(f, Loader=yaml.SafeLoader)
f.close()

iris_dataset = pd.read_csv(params['DATASET'])

iris_dataset.loc[iris_dataset["species"]=="setosa","species"]=0
iris_dataset.loc[iris_dataset["species"]=="versicolor","species"]=1
iris_dataset.loc[iris_dataset["species"]=="virginica","species"]=2

# Break the dataset up into the examples (X) and their labels (y)
X = iris_dataset.iloc[:, 0:4].values
y = iris_dataset.iloc[:, 4].values

joblib.dump(X, params['DUMPED_DATA'], compress = 3)

X = normalize(X,axis=0)

# Split up the X and y datasets randomly into train and test sets
# 20% of the dataset will be used for the test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=31)

#Change the label to one hot vector
'''
[0]--->[1 0 0]
[1]--->[0 1 0]
[2]--->[0 0 1]
'''
y_train=np_utils.to_categorical(y_train, num_classes = 3)
y_test=np_utils.to_categorical(y_test, num_classes = 3)

# Initialising the ANN
model = Sequential()

# Adding the input layer and the first hidden layer
model.add(Dense(1000, input_dim=4, activation='relu'))

#Changing number of nodes in first hidden layer
model.add(Dense(50, activation = 'relu'))

# Adding the second hidden layer
model.add(Dense(300, activation = 'relu'))

#Protects against overfitting
model.add(Dropout(0.2))

# Adding the output layer
model.add(Dense(3, activation = 'softmax'))

# Compiling the ANN
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

# Fitting the ANN to the Training set
model.fit(X_train, y_train, validation_data = (X_test, y_test), batch_size = 20, epochs = 50, verbose = 1)
model.save(params['MODEL'])

prediction = model.predict(X_test)
length = len(prediction)
y_label = np.argmax(y_test, axis = 1)
predict_label = np.argmax(prediction, axis = 1)

# How times it matched/ how many test cases
accuracy = np.sum(y_label == predict_label) / length * 100 
print("Accuracy of the dataset", accuracy )
