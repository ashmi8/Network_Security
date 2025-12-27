from Network_security.components.data_transformation import DataTransformation
from Network_security.exception.exception import NetworkSecurityException
from Network_security.logging.logger import logging
from Network_security.components.data_ingestion import DataIngestion
from Network_security.components.data_validation import DataValidation
from Network_security.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig, DataValidationConfig,DataTransformationConfig

import sys


if __name__ == "__main__":
    try:
        ## Initialize the training pipeline configuration
        training_pipeline_config = TrainingPipelineConfig()
        ## Initialize the data ingestion configuration
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        ## Start the data ingestion process
        logging.info("Starting data ingestion process")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
        print(data_ingestion_artifact)
        ## Start the data validation process
        logging.info("Starting data validation process")
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                            data_validation_config=data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        logging.info(f"Data validation artifact: {data_validation_artifact}")
        ### Start the data transformation process
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        logging.info("data Transformation started")
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("data Transformation completed")
    except Exception as e:
        raise NetworkSecurityException(e, sys)