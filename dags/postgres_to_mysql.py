from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

def replicate_postgres_to_mysql():
    pg_engine = create_engine("postgresql+psycopg2://postgres:root@postgres:5432/testdb")
    mysql_engine = create_engine("mysql+pymysql://root:root@mysql:3306/testdb")

    # Читаем данные из PostgreSQL
    df = pd.read_sql("SELECT * FROM customers", con=pg_engine)

    # Пишем в MySQL (перезаписываем таблицу)
    df.to_sql("customers", con=mysql_engine, if_exists="replace", index=False)

with DAG(
    dag_id="postgres_to_mysql",
    default_args=default_args,
    description="Replicate customers from PostgreSQL to MySQL",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    tags=["replication"]
) as dag:

    replicate_task = PythonOperator(
        task_id="replicate_postgres_to_mysql",
        python_callable=replicate_postgres_to_mysql
    )
