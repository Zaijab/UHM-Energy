# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


import tensorflow as tf

class EncoderDecoder(tf.keras.layers.Layer):
    
    def __init__(self, units):
        
        '''
        LSTM Encoder-Decoder layer, see Section 2.1 of the EncDec-AD paper.
        Parameters:
        __________________________________
        units: int.
            Number of hidden units.
        '''
        
        self.units = units
        self.encoder = None
        self.decoder = None
        self.outputs = None
        super(EncoderDecoder, self).__init__()
    
    def build(self, input_shape):

        if self.encoder is None:
            self.encoder = tf.keras.layers.LSTM(units=self.units)
        
        if self.decoder is None:
            self.decoder = tf.keras.layers.LSTMCell(units=self.units)

        if self.outputs is None:
            self.outputs = tf.keras.layers.Dense(units=input_shape[-1])

    def call(self, inputs, training=True):
    
        '''
        Parameters:
        __________________________________
        inputs: tf.Tensor.
            Model inputs (actual time series), tensor with shape (samples, timesteps, features) where samples
            is the batch size, timesteps is the number of time steps and features is the number of time series.
        
        training: bool.
            Whether the call is in training mode (True) or inference mode (False).
            
        Returns:
        __________________________________
        outputs: tf.Tensor.
            Model outputs (reconstructed time series), tensor with shape (samples, timesteps, features) where samples
            is the batch size, timesteps is the number of time steps and features is the number of time series.
        '''
        
        # Initialize the outputs.
        y = tf.TensorArray(
            element_shape=(inputs.shape[0], inputs.shape[2]),
            size=inputs.shape[1],
            dynamic_size=False,
            dtype=tf.float32,
            clear_after_read=False
        )
        
        # Get the inputs.
        x = tf.cast(inputs, dtype=tf.float32)
        
        # Update the encoder states.
        he = self.encoder(x)

        # Initialize the decoder states.
        hd = tf.identity(he)
        cd = tf.zeros(shape=(tf.shape(inputs)[0], self.units))
        
        # Update the decoder states.
        for t in tf.range(start=inputs.shape[1] - 1, limit=-1, delta=-1):
            y = y.write(index=t, value=self.outputs(hd))
            hd, [hd, cd] = self.decoder(states=[hd, cd], inputs=x[:, t, :] if training else y.read(index=t))

        # Return the outputs.
        return tf.transpose(y.stack(), (1, 0, 2))

import numpy as np
import pandas as pd
import tensorflow as tf

class EncDecAD():
    
    def __init__(self, x, units, timesteps):
    
        '''
        Implementation of multivariate time series anomaly detection model introduced in Malhotra, P., Ramakrishnan, A.,
        Anand, G., Vig, L., Agarwal, P. and Shroff, G., 2016. LSTM-based encoder-decoder for multi-sensor anomaly detection.
        Parameters:
        __________________________________
        x: np.array.
            Time series, array with shape (samples, features) where samples is the length of the time series and features
            is the number of time series.
        units: int.
            Number of hidden units of the LSTM layers.
            
        timesteps: int.
            Number of time steps.
        '''
        
        self.x = x
        self.x_min = np.min(x, axis=0)
        self.x_max = np.max(x, axis=0)
        self.samples = x.shape[0]
        self.features = x.shape[1]
        self.units = units
        self.timesteps = timesteps

    def fit(self, learning_rate=0.001, batch_size=32, epochs=100, verbose=True):
        
        '''
        Train the model.
        Parameters:
        __________________________________
        learning_rate: float.
            Learning rate.
        batch_size: int.
            Batch size.
        epochs: int.
            Number of epochs.
        verbose: bool.
            True if the training history should be printed in the console, False otherwise.
        '''
    
        # Scale the time series.
        x = (self.x - self.x_min) / (self.x_max - self.x_min)

        # Generate the input sequences.
        dataset = tf.keras.utils.timeseries_dataset_from_array(
            data=tf.cast(x, tf.float32),
            targets=None,
            sequence_length=self.timesteps,
            sequence_stride=self.timesteps,
            batch_size=batch_size,
            shuffle=True
        )
        
        # Build the model.
        inputs = tf.keras.layers.Input(shape=(self.timesteps, self.features))
        outputs = EncoderDecoder(units=self.units)(inputs)
        model = tf.keras.models.Model(inputs, outputs)
        
        # Define the training loop.
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

        @tf.function
        def train_step(data):
            with tf.GradientTape() as tape:
                
                # Calculate the loss.
                output = model(data, training=True)
                loss = tf.reduce_mean(tf.reduce_sum((data - output) ** 2, axis=-1))
        
            # Calculate the gradient.
            gradient = tape.gradient(loss, model.trainable_variables)
    
            # Update the weights.
            optimizer.apply_gradients(zip(gradient, model.trainable_variables))
    
            return loss

        # Train the model.
        for epoch in range(epochs):
            for data in dataset:
                loss = train_step(data)
            if verbose:
                print('epoch: {}, loss: {:,.6f}'.format(1 + epoch, loss))

        # Save the model.
        self.model = model

    def predict(self, x):
    
        '''
        Reconstruct the time series and score the anomalies.
        Parameters:
        __________________________________
        x: np.array.
            Actual time series, array with shape (samples, features) where samples is the length
            of the time series and features is the number of time series.
        Returns:
        __________________________________
        x_hat: np.array.
            Reconstructed time series, array with shape (samples, features) where samples is the
            length of the time series and features is the number of time series.
    
        scores: np.array.
            Anomaly scores, array with shape (samples,) where samples is the length of the time
            series.
        '''
    
        if x.shape[1] != self.features:
            raise ValueError(f'Expected {self.features} features, found {x.shape[1]}.')
    
        else:

            # Generate the reconstructions.
            dataset = tf.keras.utils.timeseries_dataset_from_array(
                data=tf.cast((x - self.x_min) / (self.x_max - self.x_min), tf.float32),
                targets=None,
                sequence_length=self.timesteps,
                sequence_stride=self.timesteps,
                batch_size=1,
                shuffle=False
            )
        
            x_hat = np.concatenate([self.model(data, training=False).numpy() for data in dataset], axis=0)
            x_hat = np.concatenate([x_hat[i, :, :] for i in range(x_hat.shape[0])], axis=0)
            x_hat = self.x_min + (self.x_max - self.x_min) * x_hat

            # Calculate the anomaly scores.
            errors = np.abs(x - x_hat)
            mu = np.mean(errors, axis=0)
            sigma = np.cov(errors, rowvar=False)
            scores = np.array([np.dot(np.dot((errors[i, :] - mu).T, np.linalg.inv(sigma)), (errors[i, :] - mu)) for i in range(errors.shape[0])])

            return x_hat, scores

data = pd.read_csv("../data/power_average.csv")
data = data.set_index(["building_name","datetime"])
data["day_type"] = pd.Categorical(data["day_type"]).codes

x = data.to_numpy()

# Fit the model
model = EncDecAD(
    x=x,
    units=100,
    timesteps=200
)

model.fit(
    learning_rate=0.001,
    batch_size=32,
    epochs=500,
    verbose=True
)

# Score the anomalies
x_hat, scores = model.predict(x=x)

