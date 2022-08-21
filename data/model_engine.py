import os
import numpy as np
from tensorflow import keras
from keras.models import load_model
from keras.utils import to_categorical


def retrain(retrain_data):
    file_name = os.path.dirname(__file__) + '\\saved_model\\model.h5'
    model = load_model(file_name)

    train_x = np.asarray([measurement[5:] for measurement in retrain_data])
    train_y = np.asarray([measurement[2] for measurement in retrain_data])

    train_x = np.reshape(train_x, (train_x.__len__(), 28, 1))
    train_y = to_categorical(train_y - 1)

    model.summary()
    model.compile(
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        optimizer=keras.optimizers.RMSprop(),
        metrics=['accuracy']
    )
    model.fit(train_x, train_y, epochs=50, validation_split=0.2, batch_size=400)

    model.save('trained_model.h5')
    print("Model saved!")


def predict(measurement):
    file_name = os.path.dirname(__file__) + '\\saved_model\\model.h5'
    model = load_model(file_name)

    measurement_data = np.asarray(measurement[5:])
    measurement_data = np.reshape(measurement_data, (1, 28, 1))
    correct_class = np.asarray([measurement[2]])

    prediction = model.predict(measurement_data)
    result = np.argmax(prediction, axis=1)[0] + 1
    probability = prediction.max(1)[0] * 100

    return int(result), int(probability)
