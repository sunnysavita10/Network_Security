import os
import sys

from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logger.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

models = {
    'XG Boost' : XGBClassifier(),
    'Random Forest' : RandomForestClassifier()
} 

hyper_params = {
    "XG Boost" : {
        'learning_rate' : [10, 1, 0.1, 0.01, 0.001],
        'n_estimators' : [8, 16, 32, 64, 128, 256]
    },
    "Random Forest" : {
        'n_estimators' : [8, 16, 32, 64, 128, 256]
    }
}

class ModelTrainer:

    def __init__(self,model_trainer_config:ModelTrainerConfig,
        data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def evaluate_models(self, X_train, y_train, X_test, y_test, models, params):
        try:
            report = {}

            for i in range(len(list(models))):
                model = list(models.values())[i]
                param = params[list(models.keys())[i]]

                gs = GridSearchCV(model, param, cv=3)
                gs.fit(X_train, y_train)

                model.set_params(**gs.best_params_)
                model.fit(X_train, y_train)

                y_train_pred = model.predict(X_train)

                y_test_pred = model.predict(X_test)

                train_model_score = f1_score(y_train, y_train_pred)

                test_model_score = f1_score(y_test, y_test_pred)

                print(f"train score {model}", train_model_score)
                print(f"test score {model}", test_model_score)

                report[list(models.keys())[i]] = test_model_score

            return report
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def perform_hyper_parameter_tunig(self, X_train, y_train, X_test, y_test):
        try:
            model_report : dict = self.evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, params=hyper_params)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            print(f'----{best_model_name}')
            best_model = models[best_model_name]
            print(best_model)
            return best_model
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self,x_train,y_train, best_model):
        try:
            clf = best_model
            clf.fit(x_train, y_train)
            return clf
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            best_model = self.perform_hyper_param_tuning(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
            print("-"*10)
            print(best_model)
            print("-"*20)
            model = self.train_model(x_train, y_train, best_model)
            y_train_pred = model.predict(x_train)
            classification_train_metric =  get_classification_score(y_true=y_train, y_pred=y_train_pred)
            
            if classification_train_metric.f1_score<=self.model_trainer_config.expected_accuracy:
                raise Exception("Trained model is not good to provide expected accuracy")
            
            y_test_pred = model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)


            #Overfitting and Underfitting
            diff = abs(classification_train_metric.f1_score-classification_test_metric.f1_score)
            
            if diff>self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is not good try to do more experimentation.")

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            Network_Model = NetworkModel(preprocessor=preprocessor,model=model)
            save_object(self.model_trainer_config.trained_model_file_path, obj=Network_Model)

            #model trainer artifact

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path, 
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)