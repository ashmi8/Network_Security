from Network_security.exception.exception import NetworkSecurityException
from Network_security.logging.logger import logging

## imports for data ingestino config 
from Network_security.entity.config_entity import DataIngestionConfig
from Network_security.entity.artifacts_entity import DataIngestionArtifact
import os
import sys
import pandas as pd
import numpy as np
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()

MONOGO_DB_URL = os.getenv("MONGODB_URI")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
    
    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Export MongoDB collection as a pandas dataframe
        """
        try:
            logging.info("Exporting collection data as dataframe")
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONOGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]    

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace({'na':np.nan},inplace=True)

            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_into_feature_store(self, df: pd.DataFrame) -> str:
        """
        Export DataFrame into feature store
        """
        try:
            logging.info("Exporting data into feature store")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            feature_store_dir = os.path.dirname(feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            df.to_csv(feature_store_file_path, index=False, header=True)
            return df 
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, df: pd.DataFrame):
        try:
            train_set,test_set=  train_test_split(
                df,
                test_size=self.data_ingestion_config.train_test_split_ratio,
            )
            logging.info("Splitting data into train and test set")
            logging.info("Exited split_data_as_train_test method of Data Ingestion class")

            dir_path=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info("Exporting train and test file")
            train_set.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            logging.info("Exported train and test file successfully")
            logging.info(
                f"Train file path : {self.data_ingestion_config.train_file_path} \n test file path : {self.data_ingestion_config.test_file_path}"
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact=DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path,
            )
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
