import os 
import sys
from src.logger import logging
from src.exception import CustomException

# Import required libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Initialize the Data Ingestion Configuration
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'raw.csv')

# Create the Data Ingestion Class
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Started")
        try:
            # Read the dataset
            df = pd.read_csv(os.path.join('notebooks', 'data', 'gemstone.csv'))
            logging.info("Data read successfully")
            
            # Create artifacts directory
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            print(f"Saving raw data to: {self.ingestion_config.raw_data_path}")
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Raw data is created successfully")

            # Split the data into train and test sets
            train_set, test_set = train_test_split(df, test_size=0.30, random_state=42)

            print(f"Saving train data to: {self.ingestion_config.train_data_path}")
            print(f"Saving test data to: {self.ingestion_config.test_data_path}")

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of data completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.info("Error occurred in data ingestion")
            raise CustomException(e, sys)
