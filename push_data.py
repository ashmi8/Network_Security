import os
from dotenv import load_dotenv
import sys
import certifi
import pymongo
import pandas as pd
from Network_security.exception.exception import NetworkSecurityException
import json

load_dotenv()

MONGO_DB_URL = os.getenv("MONGODB_URI")
print(MONGO_DB_URL)  # for checking if the url is loading properly

ca=certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
        
    def csv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_to_mongoDB(self,records,database_name,collection_name):
        try:
            self.database_name=database_name
            self.collection_name=collection_name
            self.records=records
            self.client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.client[self.database_name]
            self.collection = self.database[self.collection_name]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

if __name__ == "__main__":
    FILE_PATH="Network_Data/phisingData.csv"
    DATABAWSE_NAME="ASHMI_DB"
    COLLECTION_NAME="NetworkData"
    obj=NetworkDataExtract()
    records=obj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)
    number_of_records_inserted=obj.insert_data_to_mongoDB(records=records,database_name=DATABAWSE_NAME,collection_name=COLLECTION_NAME)
    print(f"Number of records inserted: {number_of_records_inserted}")

