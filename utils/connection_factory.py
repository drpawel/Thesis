import mysql.connector

password = ''


def create_initial_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password=password
    )


def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='thesis'
    )
