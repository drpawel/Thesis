import numpy as np
from tensorflow import keras
from keras.models import load_model

model = load_model('saved_model/model.h5')
model.summary()
model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=keras.optimizers.RMSprop(),
    metrics=["accuracy"]
)

# temporary data for userid=4
dd = np.asarray([0.39418201, 0.03036661, 0.03819507, 0.42105263, 0.03381043, 0.04486094, 0.34664634,
                0.00845843, 0.01013583, 0.43179709, 0.23933071, 0.23788047, 0.57316456, 0.17511706,
                0.17126944, 0.37566893, 0.17295084, 0.18026107, 0.13920329, 0.07438277, 0.11192878,
                0.06444149, 0.04427811, 0.0902272, 0.25282486, 0.08703, 0.10450169, 0.38605341])
dd = np.reshape(dd, (1, 28, 1))

prediction = model.predict(dd)
result = np.argmax(prediction, axis=1)[0] + 1
probability = prediction.max(1)[0] * 100
print('Result {} with probability: {}'.format(result, probability))
