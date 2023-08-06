from os import getenv
from typing import Iterator

from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv


class DataModelMongo:
    """ MongoDB Data Model """
    load_dotenv()
    db_url = getenv('DB_URL')
    collection = getenv('DB_COLLECTION')
    table = getenv('DB_TABLE')

    def connect(self):
        return MongoClient(self.db_url)[self.collection][self.table]

    def find(self, query_obj: dict) -> dict:
        return self.connect().find_one(query_obj)

    def insert(self, insert_obj: dict):
        self.connect().insert_one(insert_obj)

    def find_many(self, query_obj: dict, limit=5000) -> Iterator[dict]:
        return self.connect().find(query_obj, limit=limit)

    def insert_many(self, insert_obj: dict):
        self.connect().insert_many(insert_obj)

    def update(self, query: dict, data: dict):
        self.connect().update_one(query, {"$set": data})

    def get_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.find_many({}))


if __name__ == '__main__':
    db = DataModelMongo()
    print(db.get_df())
