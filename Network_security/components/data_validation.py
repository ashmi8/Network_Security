from Network_security.exception.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.entity.config_entity import DataValidationConfig
from Network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from Network_security.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
import os, sys
from scipy.stats import ks_2samp
import pandas as pd
from Network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Expected number of columns: {number_of_columns}, Found: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def detect_dataset_drift(self, base_dataframe: pd.DataFrame,
                            current_dataframe: pd.DataFrame,
                            threshold: float = 0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_dataframe.columns:
                d1 = base_dataframe[column]
                d2 = current_dataframe[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = True
                else:
                    is_found = False
                    status = False
                report.update({column:{
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }})

            drift_report_file_path = self.data_validation_config.drift_report_file_path

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read data from the train and test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # validate number of columns
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = f"Train file: {train_file_path} does not contain all columns."
            
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"Test file: {test_file_path} does not contain all columns."

            # detect data drift
            status = self.detect_dataset_drift(base_dataframe=train_dataframe,
                                                  current_dataframe=test_dataframe)
            if not status:
                logging.info(f"Data drift found between train and test dataset")
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True
                                  )
            
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True
                                 )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
