import pandas as pd
from airflow.hooks.base import BaseHook
from airflow.sensors.base import BaseSensorOperator
import psycopg2


class CheckDataSensor(BaseSensorOperator):
    def __init__(self, table_name, conn_id, min_rows=1, check_date_column=None, **kwargs):

        self.conn_id = conn_id
        self.table_name = table_name
        self.min_rows = min_rows
        super().__init__(**kwargs)

    def poke(self, context):

        connection = BaseHook.get_connection(self.conn_id)

        conn = psycopg2.connect(
            dbname=connection.schema,
            user=connection.login,
            password=connection.password,
            host=connection.host,
            port=connection.port
        )
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        row_count = cur.fetchone()[0]

        cur.close()
        conn.close()

        self.log.info(f"Table {self.table_name} has {row_count} rows")

        return row_count >= self.min_rows
