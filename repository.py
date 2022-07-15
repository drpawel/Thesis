import json
import uuid

import mysql.connector


def connect():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='thesis'
    )


def insert_measurement(measurement, session_id):
    conn = connect()
    cursor = conn.cursor()

    measurement_id = uuid.uuid4()
    user_id = insert_user(cursor, measurement.get('userName'))
    conn.commit()

    insert_measurement_query = 'INSERT INTO measurements (external_id, session_id, is_training, key_events, user_id)' \
                               'VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), %s, JSON_ARRAY(%s), %s)'

    data = (measurement_id.hex,
            session_id,
            int(measurement.get('isTraining')),
            json.dumps(measurement.get('keyEvents')),
            user_id)

    cursor.execute(insert_measurement_query, data)
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
