import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.model_evaluation import ModelEvaluation
from networksecurity.components.model_pusher import ModelPusher

from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig
   
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact,
    ModelPusherArtifact
)


class TrainingPipeline:
    def __init__(self):
        pass
    
    def start_data_ingestion(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    

