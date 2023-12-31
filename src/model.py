"""
This file holds the model architecture
"""

from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import sys
import os

# importing MLFlow
import mlflow
import mlflow.keras
from mlflow.models.signature import infer_signature

# importing custom libs
from core.model.abs_model import abs_model

class mnist_model(abs_model):

    def __init__(self):

        # Model / data parameters
        self.num_classes = 10
        self.input_shape = (28, 28, 1)

        self.batch_size = 128
        self.epochs = 2

        self.data = './data/'
        self.model = './model/model.sav'


    def load_data(self,**kwargs):

        print('THIS IS MY CURRENT DIRECTORY :',os.getcwd())

        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        np.save(self.data + 'x_train.npy', x_train)
        np.save(self.data + 'y_train.npy', y_train)
        np.save(self.data + 'x_test.npy', x_test)
        np.save(self.data + 'y_test.npy', y_test)

        return 'LOADED DATA'

    def prep_data(self, **kwargs):

        x_train = np.load(self.data + 'x_train.npy')
        y_train = np.load(self.data + 'y_train.npy')
        x_test = np.load(self.data + 'x_test.npy')
        y_test = np.load(self.data + 'y_test.npy')

        # Scale images to the [0, 1] range
        x_train = x_train.astype("float32") / 255
        x_test = x_test.astype("float32") / 255
        # Make sure images have shape (28, 28, 1)
        x_train = np.expand_dims(x_train, -1)
        x_test = np.expand_dims(x_test, -1)
        print("x_train shape:", x_train.shape)
        print(x_train.shape[0], "train samples")
        print(x_test.shape[0], "test samples")

        # convert class vectors to binary class matrices
        y_train = keras.utils.to_categorical(y_train, self.num_classes)
        y_test = keras.utils.to_categorical(y_test, self.num_classes)

        np.save(self.data + 'x_train_p.npy', x_train)
        np.save(self.data + 'y_train_p.npy', y_train)
        np.save(self.data + 'x_test_p.npy', x_test)
        np.save(self.data + 'y_test_p.npy', y_test)

        return 'PREPROCESSED DATA'

    def build_model(self, **kwargs):

        model = keras.Sequential(
            [
                keras.Input(shape=self.input_shape),
                layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Flatten(),
                layers.Dropout(0.5),
                layers.Dense(self.num_classes, activation="softmax"),
            ]
        )

        model.summary()

        model.save(self.model)

        return "MODEL IS BUILT"

    def train_model(self, **kwargs):

        x_train = np.load(self.data + 'x_train_p.npy')
        y_train = np.load(self.data + 'y_train_p.npy')

        model = keras.models.load_model(self.model)
        model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        model.fit(x_train, y_train, batch_size=self.batch_size, epochs=self.epochs, validation_split=0.1)

        self.train_score = model.evaluate(x_train, y_train, verbose=0)

        model.save(self.model)

        return "MODEL IS TRAINED"

    def test_model(self, **kwargs):

        model = keras.models.load_model(self.model)
        x_test = np.load(self.data + 'x_test_p.npy')
        y_test = np.load(self.data + 'y_test_p.npy')

        signature = infer_signature(x_test, model.predict(x_test))
        mlflow.keras.log_model(model, "mnist_cnn", signature=signature)

        self.test_score = model.evaluate(x_test, y_test, verbose=0)

        return "MODEL IS TESTED"

    def log_model(self):

        # Initializing MLFlow
        try:
            # Creating an experiment
            mlflow.create_experiment('mnist_model_flow')
        except:
            pass

        model = keras.models.load_model(self.model)

        # Setting the environment with the created experiment
        mlflow.set_tracking_uri("http://0.0.0.0:5000")
        mlflow.set_experiment('mnist_model_flow')
        mlflow.start_run()

        for i in range(len(model.metrics_names)):
            mlflow.log_metric('test_' + model.metrics_names[i], test_score[i])
            mlflow.log_metric('train_' + model.metrics_names[i], train_score[i])

        mlflow.end_run()

    def serve_model(self):
        pass