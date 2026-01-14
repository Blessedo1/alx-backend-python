"""fetches rows one by one from a table using a generator"""

import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vagabodo",
            database="ALX_prodev"
            )
    cursor = connection.cursor
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()
