import os 
import sys
from pathlib import Path 
import shutil
from training.exception import DataIngestionError,handle_exception
from training.custom_logging import info_logger,error_logger
from training.entity.config_entity import DataIngestionConfig
from training.configuration_manager.configuration import ConfigurationManager

class DataIngestion:
    def __init__(self, config):
        try:
            self.config = config
            # Ensure the data directory exists
            if not os.path.exists(self.config.data_dir):
                os.makedirs(self.config.data_dir)
        except Exception as e:
            handle_exception(e, DataIngestionError)

    def save_data(self):
        try:
            # Ensure the directory for status.txt exists
            status_dir = os.path.dirname(self.config.STATUS_FILE)
            if not os.path.exists(status_dir):
                os.makedirs(status_dir)

            # Ensure the data directory exists before copying
            if not os.path.exists(self.config.data_dir):
                os.makedirs(self.config.data_dir)

            data_file_path = os.path.join(self.config.data_dir, "advertising_data.csv")

            if not os.path.exists(data_file_path):  # Check if the file exists
                if os.path.exists(self.config.source):  # Check if source exists
                    shutil.copy(self.config.source, self.config.data_dir)
                    info_logger.info(f"Data ingestion completed successfully and file copied to {self.config.data_dir}")
                else:
                    error_logger.error(f"Source file does not exist: {self.config.source}")
                    raise FileNotFoundError(f"Source file {self.config.source} not found.")
            else:
                info_logger.info(f"Data file already exists at {data_file_path}, skipping copy.")

            # Write the status file after the operation
            status = True  # Indicating success
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Data Ingestion status: {status}")

        except Exception as e:
            handle_exception(e, DataIngestionError)


if __name__ == "__main__":
    # Initialize the ConfigurationManager and retrieve the data ingestion config
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()

    # Create a DataIngestion object and call the save_data method
    data_ingestion = DataIngestion(config=data_ingestion_config)
    data_ingestion.save_data()
