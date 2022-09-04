import uuid

from data import data_formatter, connection_provider, model_engine


def insert_measurement(measurement, session_id):
    conn = connection_provider.create_connection()
    cursor = conn.cursor()

    user_id = insert_user(cursor, measurement.get('userName'))
    conn.commit()

    insert_data_query = 'INSERT INTO measurements (external_id, user_id, session_id, is_training, H_period, ' \
                        'DD_period_t, UD_period_t, H_t, DD_t_i, UD_t_i, H_i, DD_i_e, UD_i_e, H_e, DD_e_five, ' \
                        'UD_e_five, H_five, DD_five_Shift_r, UD_five_Shift_r, H_Shift_r, DD_Shift_r_o, UD_Shift_r_o, ' \
                        'H_o, DD_o_a, UD_o_a, H_a, DD_a_n, UD_a_n, H_n, DD_n_l, UD_n_l, H_l) VALUES (UUID_TO_BIN(%s), ' \
                        '%s, UUID_TO_BIN(%s), %s, %s, %s ,%s, %s, %s, %s ,%s, %s, %s, %s ,%s, %s, %s, %s ,%s, %s, %s, ' \
                        '%s ,%s, %s, %s, %s ,%s, %s, %s, %s, %s, %s) '

    measurement_id = uuid.uuid4()
    data = get_data(measurement, measurement_id, session_id, user_id)

    cursor.execute(insert_data_query, data)
    conn.commit()
    conn.close()
    return measurement_id


def insert_user(cursor, user_name):
    cursor.execute('SELECT id FROM users WHERE user_name = %s', (user_name,))
    user_id = cursor.fetchone()

    if not user_id:
        cursor.execute('INSERT INTO users (user_name) VALUES (%s)', (user_name,))
        return cursor.lastrowid
    else:
        return user_id[0]


def get_data(measurement, measurement_id, session_id, user_id):
    key_events = measurement.get('keyEvents')

    data = (measurement_id.hex,
            user_id,
            session_id,
            int(measurement.get('isTraining')),) + data_formatter.retrieve_data(key_events)
    return data


def retrain_model(session_id):
    conn = connection_provider.create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM measurements WHERE session_id = UUID_TO_BIN(%s) AND is_training= %s',
                   (session_id, 1))
    training_data = cursor.fetchall()
    conn.commit()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.commit()
    conn.close()

    model_engine.retrain(training_data, users)


def get_results(measurement_id):
    conn = connection_provider.create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM measurements WHERE external_id = UUID_TO_BIN(%s)', (measurement_id,))
    measurement = cursor.fetchone()
    conn.commit()
    conn.close()

    return model_engine.predict(measurement)
