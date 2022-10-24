import numpy as np
from pathlib import Path
from tensorflow import keras
from keras.models import load_model
from keras import layers
from sklearn.model_selection import train_test_split


def retrain(retrain_data, users):
    file_name = Path(__file__).parent.parent.__str__() + '\\data\\saved_model\\model.h5'
    model = load_model(file_name)

    data = np.asarray([measurement[4:] for measurement in retrain_data])
    labels = np.asarray([measurement[2] for measurement in retrain_data])

    data = np.reshape(data, (data.__len__(), 28, 1))
    labels = labels - 1

    train_x, test_x, train_y, test_y = train_test_split(data, labels, test_size=0.20)

    model.pop()
    model.add(layers.Dense(users.__len__(), activation='softmax'))

    model.summary()
    model.compile(
        loss=keras.losses.SparseCategoricalCrossentropy(),
        optimizer=keras.optimizers.RMSprop(),
        metrics=['accuracy'],
    )

    model.fit(train_x, train_y, epochs=250, validation_split=0.2, batch_size=400)
    test_scores = model.evaluate(test_x, test_y, verbose=2)
    print('Test loss:', test_scores[0])
    print('Test accuracy:', test_scores[1])

    model.save('data/saved_model/model.h5')
    print('Model saved!')


def predict(measurement):
    if measurement is None:
        return int(-1), int(0)

    file_name = Path(__file__).parent.parent.__str__() + '\\data\\saved_model\\model.h5'
    model = load_model(file_name)

    measurement_data = np.asarray(measurement[4:])
    measurement_data = np.reshape(measurement_data, (1, 28, 1))
    correct_class = np.asarray([measurement[2]])

    model.summary()
    prediction = model.predict(measurement_data)
    result = np.argmax(prediction, axis=1)[0] + 1
    probability = prediction.max(1)[0] * 100

    if result != correct_class:
        return False, int(probability)

    return True, int(probability)
