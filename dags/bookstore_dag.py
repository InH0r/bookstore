import os
import sys
import datetime
from datetime import datetime, timedelta
from airflow import DAG
import requests

from airflow.operators.python import PythonOperator
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.model.base import Base
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "plugins"))
from books_sensor.sensor import CheckDataSensor
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.bookstore_etl import check_etl
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.model.books_sh import Shops
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.model.books_sh import Genre
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from bookstore.model.books_sh import Price



args = {
    'owner': 'person_1',
    'depends_on_past': False,
    'start_date': datetime(2025, 11, 6),
   
}

table = [Shops.__tablename__, Genre.__tablename__, Price.__tablename__]
    
with DAG(
    dag_id='books',
    default_args=args,
    schedule='@daily',
    tags =['books'],
    catchup=False,
) as dag:

  
    
    operation_1 = PythonOperator (
        task_id='operation',
        python_callable= check_etl
    
    )

   
    check_dags = []
    
    for i in table:
        check_dag = CheckDataSensor(
            task_id = f'check_dag_{i}',
            timeout = 1000,
            mode = 'reschedule',
            poke_interval = 30,
            min_rows = 1,
            conn_id = 'new_connection',
            table_name = i
            
        )
        check_dags.append(check_dag)
    operation_1 >> check_dags
