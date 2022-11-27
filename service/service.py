import uuid
from data import model_engine, repository
from utils import data_formatter


def insert_measurement(measurement):
    user_id = repository.insert_user(measurement.get('userName'))
    measurement_id = uuid.uuid4()

    data = get_data(measurement, measurement_id, user_id)
    repository.insert_measurement(data)

    return measurement_id


def get_data(measurement, measurement_id, user_id):
    return (measurement_id.hex,
            user_id,
            int(measurement.get('isTraining')),) + data_formatter.retrieve_data(measurement.get('keyEvents'))


def retrain_model():
    training_data = repository.get_all_measurements_for_training()
    users = repository.get_all_users()

    model_engine.retrain(training_data, users)


def get_result(measurement_id):
    measurement = repository.get_measurement(measurement_id)

    return model_engine.predict(measurement, 86)
