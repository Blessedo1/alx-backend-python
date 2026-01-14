#!/usr/bin/env python3
"""sets up the ALX_prodev database and populates it with data rom user_data.csv"""

import csv
import uuid
import mysql.connector
from mysql.connector import Error

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_db():
    """connects to the MySQL server"""
    return mysql.connector.connect(
            host="localhost",
            user="root",
            password="vagabodo"
            )

def create_database(connection):
    """creates the database ALX_prodev if it does not exist"""
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()

def connect_to_prodev():
    """connects to the ALX_prodev database"""
    return mysql.connector.connect(
            host="localhost",
            user="root",
            password="vagabodo",
            database=DB_NAME
            )

def create_table(connection):
    """Creates the user_data table if it does not exist"""
    cursor = connection.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX(user_id)
        )
        """
    )
    cursor.close()

def insert_data(connection, data):
    """Inserts data into the database if it does not exist"""
    cursor = connection.cursor()
    query = f"""
        INSERT IGNORE INTO {TABLE_NAME} (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
    """

    for row in data:
        cursor.execute(query, row)

    connection.commit()
    cursor.close()
