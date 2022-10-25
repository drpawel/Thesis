from utils import connection_factory


def insert_user(user_name):
    conn = connection_factory.create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE user_name = %s', (user_name,))
    user_id = cursor.fetchone()

    if not user_id:
        cursor.execute('INSERT INTO users (user_name) VALUES (%s)', (user_name,))
        user_id = cursor.lastrowid
    else:
        user_id = user_id[0]

    conn.commit()
    conn.close()
    return user_id


def insert_measurement(data):
    conn = connection_factory.create_connection()
    cursor = conn.cursor()

    insert_data_query = 'INSERT INTO measurements (external_id, user_id, is_training, H_period, DD_period_t, ' \
                        'UD_period_t, H_t, DD_t_i, UD_t_i, H_i, DD_i_e, UD_i_e, H_e, DD_e_five, UD_e_five, H_five, ' \
                        'DD_five_Shift_r, UD_five_Shift_r, H_Shift_r, DD_Shift_r_o, UD_Shift_r_o, H_o, DD_o_a, ' \
                        'UD_o_a, H_a, DD_a_n, UD_a_n, H_n, DD_n_l, UD_n_l, H_l) VALUES (UUID_TO_BIN(%s),%s, %s, %s, ' \
                        '%s ,%s, %s, %s, %s ,%s, %s, %s, %s ,%s, %s, %s, %s ,%s, %s, %s, %s ,%s, %s, %s, %s ,%s, %s, ' \
                        '%s, %s, %s, %s) '
    cursor.execute(insert_data_query, data)

    conn.commit()
    conn.close()


def get_all_measurements_for_training():
    conn = connection_factory.create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM measurements WHERE is_training=1')
    training_measurements = cursor.fetchall()

    conn.commit()
    conn.close()
    return training_measurements


def get_all_users():
    conn = connection_factory.create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    conn.commit()
    conn.close()
    return users


def get_measurement(measurement_id):
    conn = connection_factory.create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM measurements WHERE external_id = UUID_TO_BIN(%s)', (measurement_id,))
    measurement = cursor.fetchone()

    conn.commit()
    conn.close()
    return measurement
