import csv
import mysql.connector
import psycopg2
from datetime import datetime

def load_to_mysql():
    conn = mysql.connector.connect(host="localhost", user="root", password="root", database="testdb", port=3306)
    cursor = conn.cursor()
    with open("customers.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            cursor.execute(
                "INSERT INTO customers (id, full_name, email, country, created_at) VALUES (%s, %s, %s, %s, %s)",
                (
                    int(row["id"]),
                    row["full_name"],
                    row["email"],
                    row["country"],
                    datetime.fromisoformat(row["created_at"])
                )
            )
    conn.commit()
    conn.close()

def load_to_postgres():
    conn = psycopg2.connect(host="localhost", user="postgres", password="root", dbname="testdb", port=5432)
    cursor = conn.cursor()
    with open("customers.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            cursor.execute(
                "INSERT INTO customers (id, full_name, email, country, created_at) VALUES (%s, %s, %s, %s, %s)",
                (
                    int(row["id"]),
                    row["full_name"],
                    row["email"],
                    row["country"],
                    datetime.fromisoformat(row["created_at"])
                )
            )
    conn.commit()
    conn.close()

# Запускаем оба варианта
load_to_mysql()
load_to_postgres()
