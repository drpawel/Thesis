import csv
import uuid
from data import connection_provider

conn = connection_provider.create_connection()
cursor = conn.cursor()
user_ids = {}

create_users_table = 'CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, user_name VARCHAR(100) UNIQUE NOT NULL)'
cursor.execute(create_users_table)
conn.commit()

create_measurement_table = 'CREATE TABLE measurements (id INT PRIMARY KEY AUTO_INCREMENT, external_id BINARY(16) ' \
                           'UNIQUE NOT NULL, user_id INT, FOREIGN KEY (user_id) REFERENCES users(id), is_training BOOLEAN NOT NULL, H_period FLOAT, DD_period_t ' \
                           'FLOAT, UD_period_t FLOAT, H_t FLOAT, DD_t_i FLOAT, UD_t_i FLOAT, H_i FLOAT, DD_i_e FLOAT, ' \
                           'UD_i_e FLOAT, H_e FLOAT, DD_e_five FLOAT, UD_e_five FLOAT, H_five FLOAT, DD_five_Shift_r ' \
                           'FLOAT, UD_five_Shift_r FLOAT, H_Shift_r FLOAT, DD_Shift_r_o FLOAT, UD_Shift_r_o FLOAT, ' \
                           'H_o FLOAT, DD_o_a FLOAT, UD_o_a FLOAT, H_a FLOAT, DD_a_n FLOAT, UD_a_n FLOAT, H_n FLOAT, ' \
                           'DD_n_l FLOAT, UD_n_l FLOAT, H_l FLOAT) '

cursor.execute(create_measurement_table)
conn.commit()


def insert_user(users_set):
    for user_name in users_set:
        cursor.execute('INSERT INTO users (user_name) VALUES (%s)', (user_name,))
        user_ids[user_name] = cursor.lastrowid

    conn.commit()
    return user_ids


with open('../resources/DSL-StrongPasswordData.csv', 'r') as file:
    reader = csv.DictReader(file)

    users = set()
    for i in reader:
        users.add(i['subject'])

    users_names = insert_user(users)

with open('../resources/DSL-StrongPasswordData.csv', 'r') as file:
    reader = csv.DictReader(file)

    data = [(uuid.uuid4().hex, user_ids.get(i['subject']), True, i['H.period'],
             i['DD.period.t'], i['UD.period.t'], i['H.t'], i['DD.t.i'], i['UD.t.i'], i['H.i'], i['DD.i.e'], i['UD.i.e'],
             i['H.e'], i['DD.e.five'], i['UD.e.five'], i['H.five'], i['DD.five.Shift.r'], i['UD.five.Shift.r'],
             i['H.Shift.r'], i['DD.Shift.r.o'], i['UD.Shift.r.o'], i['H.o'], i['DD.o.a'], i['UD.o.a'], i['H.a'],
             i['DD.a.n'], i['UD.a.n'], i['H.n'], i['DD.n.l'], i['UD.n.l'], i['H.l']) for i in reader]

    insert_data_query = 'INSERT INTO measurements (external_id, user_id, is_training, H_period, ' \
                        'DD_period_t, UD_period_t, H_t, DD_t_i, UD_t_i, H_i, DD_i_e, UD_i_e, H_e, DD_e_five, ' \
                        'UD_e_five, H_five, DD_five_Shift_r, UD_five_Shift_r, H_Shift_r, DD_Shift_r_o, UD_Shift_r_o, ' \
                        'H_o, DD_o_a, UD_o_a, H_a, DD_a_n, UD_a_n, H_n, DD_n_l, UD_n_l, H_l) VALUES (UUID_TO_BIN(%s), ' \
                        '%s, %s, %s, %s ,%s, %s, %s, %s ,%s, %s, %s, %s ,%s, %s, %s, %s ,%s, %s, %s, ' \
                        '%s ,%s, %s, %s, %s ,%s, %s, %s, %s, %s, %s) '

    cursor.executemany(insert_data_query, data)
    conn.commit()

print("Created tables in thesis database: users, measurements")
conn.close()
