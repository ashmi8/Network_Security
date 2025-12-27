import os

'''
 Defining the common constants for training pipeline
'''

TARGET_COLUMN = 'Result'
PIPELINE_NAME: str = 'NetworkSecurity'
ARTIFACT_DIR: str = 'Artifacts'
FILE_NAME: str = 'phisingData.csv'

TRAINING_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'

SCHEMA_FILE_PATH: str = "data_schema/schema.yaml"

'''
    Data ingestion related constants start with DATA_INGESTION VARIANTS NAME
'''

DATA_INGESTION_COLLECTION_NAME: str = 'NetworkData'
DATA_INGESTION_DATABASE_NAME: str = 'ASHMI_DB'
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

'''
    Data validation related constants start with DATA_VALIDATION VARIANTS NAME
'''

DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = 'validated'
DATA_VALIDATION_INVALID_DIR: str = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'report.yaml'
