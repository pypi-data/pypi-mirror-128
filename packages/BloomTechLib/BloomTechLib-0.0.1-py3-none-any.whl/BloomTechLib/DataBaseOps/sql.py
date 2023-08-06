import os
from typing import Iterable

import psycopg2
from dotenv import load_dotenv


class DataModelSQL:
    load_dotenv()
    db_url = os.getenv('DB_URL')

    def __init__(self, table_name, columns: Iterable[str]):
        self.table_name = table_name
        self.db_action(f"""CREATE TABLE IF NOT EXISTS {self.table_name} 
        ({', '.join(columns)});""")

    def db_action(self, sql_action: str):
        """ DB Setter - Performs a DB action returns None """
        conn = psycopg2.connect(self.db_url)
        curs = conn.cursor()
        curs.execute(sql_action)
        conn.commit()
        curs.close()
        conn.close()

    def db_query(self, sql_query: str) -> list:
        """ DB Getter - Returns query result as a List """
        conn = psycopg2.connect(self.db_url)
        curs = conn.cursor()
        curs.execute(sql_query)
        results = curs.fetchall()
        curs.close()
        conn.close()
        return results


if __name__ == '__main__':

    db = DataModelSQL("testing", [
        "Id SERIAL PRIMARY KEY NOT NULL",
        "Name TEXT NOT NULL",
        "Age INT NOT NULL",
    ])
