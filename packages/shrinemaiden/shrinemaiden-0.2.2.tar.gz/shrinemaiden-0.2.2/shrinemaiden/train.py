from typing import *
from sklearn.metrics import mean_squared_error
from keras.models import Sequential

import numpy as np
import tensorflow as tf
import sklearn.metrics as metrics

class StandardTrainer:
    def __init__(
        self,
        model: Sequential,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: np.ndarray,
        y_test: np.ndarray,
    ):
        """
        Trains the model and logs the loss, accuracy, MAE, MSE, and RMSE

        PARAMETERS
        ==========
        model: Sequential
          A Keras Sequential Model
        X_train: ndarray
          A numpy array containing the X training data
        X_test: ndarray
          A numpy array containing the X testing data
        y_train: ndarray
          A numpy array containing the y training data
        y_test: ndarray
          A numpy array containing the y testing data
        """
        self.model      = model
        self.X_train    = X_train
        self.X_test     = X_test
        self.y_train    = y_train
        self.y_test     = y_test
        self.checkpoint = None
        self.callbacks  = []

        self.checkpoint_output_file = "model_checkpoint.hdf5"
  
    def set_checkpoint(self, checkpoint: tf.keras.callbacks.ModelCheckpoint):
        """
        Sets a custom checkpoint configuration for the model.
        The default checkpoint monitors the loss, saves the weights only,
        saves the best result only, and uses the min mode.

        PARAMETERS
        ==========
        checkpoint: tf.keras.callbacks.ModelCheckpoint
          The checkpoint object
        """
        self.checkpoint = checkpoint
  
    def initialize_default_checkpoint(self):
        """
        Initializes the default checkout of the model
        """
        self.checkpoint = tf.keras.callbacks.ModelCheckpoint(
            self.checkpoint_output_file,
            monitor='loss',
            save_weights_only=True,
            save_best_only = True,
            mode = 'min'
        );
  
    def set_checkpoint_output_file(self, filename: str):
        """
        Sets the name of the output file

        PARAMETERS
        ==========
        filename: str
          The name of the file
        """
        self.checkpoint_output_file = filename

    def add_callback(self, callback):
        """
        Adds a callback to the model training process

        PARAMETERS
        ==========
        callback: A Keras Callback
          The callback of the model
        """
        self.callbacks.append(callback);
    
    def train(
        self,
        batch_size: int = 1,
        epochs: int     = 1000,
        log_every: int  = 100,
        verbose: int    = 0
    ):
        """
        Trains the model

        PARAMETERS
        ==========
        batch_size: int
          DEFAULT = 1
          The batch size
        epochs: int
          DEFAULT = 1000
          The MAXIMUM epochs you want to train the model for
        log_every: int
          DEFAULT = 100
          Determines when to log the model
        verbose: int
          DEFAULT = 0
          Selects the verboseness of the training process
          0: Log only
          1: Shows Progress Bar
          2: One Line Per epoch
        """

        # Initializing the checkpoint and callback functions
        if self.checkpoint is None:
          self.initialize_default_checkpoint();
        self.callbacks.append(self.checkpoint)

        # Training the model
        for i in range(0, epochs, log_every):
          print("========================================================")
          print(f"Epoch {i}-{i+log_every}:")
          hist = self.model.fit(
              self.X_train,
              self.y_train,
              batch_size = batch_size,
              epochs = log_every,
              callbacks = self.callbacks,
              verbose = verbose
          );

          # Logs the result
          prediction_result = self.model.predict(self.X_test)
          mae = metrics.mean_absolute_error(self.y_test, prediction_result)
          rms = mean_squared_error(self.y_test, prediction_result, squared=False)
          mse = mean_squared_error(self.y_test, prediction_result)
          r2 = metrics.r2_score(self.y_test, prediction_result)

          print(f"Accuracy: {hist.history['accuracy'][-1]}")
          print(f"Loss: {hist.history['loss'][-1]}")
          print(f"MAE:{mae}")
          print(f"MSE:{mse}")
          print(f"RMSE:{rms}")
          print(f"R-Squared:{r2}")
          print("========================================================")
