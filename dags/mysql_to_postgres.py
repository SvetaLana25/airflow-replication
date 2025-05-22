from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import sqlalchemy

def replicate_mysql_to_postgres():
    mysql_engine = sqlalchemy.create_engine("mysql+pymysql://root:root@mysql:3306/testdb")
    pg_engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:root@postgres:5432/testdb")

    df = pd.read_sql("SELECT * FROM customers", con=mysql_engine)
    df.to_sql("customers", con=pg_engine, if_exists="replace", index=False)

with DAG(
    "mysql_to_postgres",
    default_args={"retries": 1, "retry_delay": timedelta(minutes=1)},
    schedule_interval="@hourly",
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    PythonOperator(
        task_id="replicate",
        python_callable=replicate_mysql_to_postgres
    )
