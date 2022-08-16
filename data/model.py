import numpy as np
import connection_provider
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras import layers
from keras.utils import to_categorical
import matplotlib.pyplot as plt


def retrieve_training_and_test_data():
    conn = connection_provider.create_connection()
    cursor = conn.cursor()

    # retrieve data from database
    cursor.execute("SELECT * FROM measurements")
    measurements = cursor.fetchall()
    conn.close()

    data = np.asarray([measurement[5:] for measurement in measurements])
    labels = np.asarray([measurement[2] for measurement in measurements])

    # normalize the dataset
    data = MinMaxScaler(feature_range=(0, 1)).fit_transform(data)
    data = np.reshape(data, (data.__len__(), 28, 1))
    labels = to_categorical(labels - 1)

    return train_test_split(data, labels, test_size=0.20)


def create_and_compile_model():
    # create model
    model = keras.Sequential()
    model.add(layers.LSTM(100, return_sequences=True, input_shape=(28, 1)))
    model.add(layers.LSTM(100, return_sequences=True))
    model.add(layers.LSTM(100))
    model.add(layers.Dense(51, activation='softmax'))

    model.summary()
    model.compile(
        loss=keras.losses.CategoricalCrossentropy(),
        optimizer=keras.optimizers.RMSprop(),
        metrics=["accuracy"],
    )
    return model


def train_and_save_model(model, train_x, test_x, train_y, test_y):
    # train model
    history = model.fit(train_x, train_y, epochs=500, validation_split=0.2, batch_size=400)

    # evaluate model
    test_scores = model.evaluate(test_x, test_y, verbose=2)
    print("Test loss:", test_scores[0])
    print("Test accuracy:", test_scores[1])

    # save model
    model.save('saved_model/model.h5')
    print("Model saved!")

    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


train_data, test_data, train_labels, test_labels = retrieve_training_and_test_data()
compiled_model = create_and_compile_model()
train_and_save_model(compiled_model, train_data, test_data, train_labels, test_labels)
