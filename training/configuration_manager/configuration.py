from training.constants import *
from training.utils.common import read_yaml, create_directories
from training.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    FeatureEngineeringConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    CrossValConfig,
)

class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH, schema_filepath=SCHEMA_FILE_PATH):
        try:
            # Reading YAML files and checking if they exist
            self.config = read_yaml(config_filepath)
            self.params = read_yaml(params_filepath)
            self.schema = read_yaml(schema_filepath)

            # Create required directories from config
            create_directories([self.config.artifacts_root])

        except Exception as e:
            raise ValueError(f"Error initializing ConfigurationManager: {str(e)}") from e

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source=config.source,
            data_dir=config.data_dir,
            STATUS_FILE=config.STATUS_FILE,
        )
        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            data_dir=config.data_dir,
            STATUS_FILE=config.STATUS_FILE,
        )

        return data_validation_config

    def get_feature_engineering_config(self) -> FeatureEngineeringConfig:
        config = self.config.feature_engineering

        create_directories([config.root_dir])

        feature_engineering_config = FeatureEngineeringConfig(
            root_dir=config.root_dir,
            train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,
            STATUS_FILE=config.STATUS_FILE,
        )

        return feature_engineering_config

    def get_cross_val_config(self) -> CrossValConfig:
        config = self.config.cross_val

        # Create directories safely, only if not existing
        create_directories([config.root_dir])
        create_directories([config.extracted_features, config.random_search_models_rf, config.model_cache_rf])
        create_directories([config.train_data_path, config.test_data_path])
        create_directories([config.metric_file_name_rf, config.best_model_params_rf])

        cross_val_config = CrossValConfig(
            root_dir=config.root_dir,
            extracted_features=config.extracted_features,
            random_search_models_rf=config.random_search_models_rf,
            model_cache_rf=config.model_cache_rf,
            train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,
            model_name=config.model_name,
            STATUS_FILE=config.STATUS_FILE,
            metric_file_name_rf=config.metric_file_name_rf,
            best_model_params_rf=config.best_model_params_rf,
        )

        return cross_val_config

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,
            metric_file_name_rf=config.metric_file_name_rf,
            best_model_params_rf=config.best_model_params_rf,
            final_model_name=config.final_model_name,
            STATUS_FILE=config.STATUS_FILE,
        )

        return model_trainer_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation

        create_directories([config.root_dir])
        create_directories([config.metric_file])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            test_data_path=config.test_data_path,
            model_path=config.model_path,
            metric_file=config.metric_file,
            STATUS_FILE=config.STATUS_FILE,
        )

        return model_evaluation_config

    