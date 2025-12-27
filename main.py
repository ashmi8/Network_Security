from Network_security.exception.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.components.data_ingestion import DataIngestion
from Network_security.components.data_validation import DataValidation
from Network_security.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig, DataValidationConfig
import sys


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Starting data ingestion process")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
        print(data_ingestion_artifact)
        logging.info("Starting data validation process")
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                            data_validation_config=data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        logging.info(f"Data validation artifact: {data_validation_artifact}")
    except Exception as e:
        raise NetworkSecurityException(e, sys)