from sklearn.impute import SimpleImputer ## HAndling Missing Values
from sklearn.preprocessing import StandardScaler # HAndling Feature Scaling
from sklearn.preprocessing import OrdinalEncoder # Ordinal Encoding
## pipelines
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

import numpy as np
import pandas as pd
import os
import sys

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

from src.utils import save_object

@dataclass
class DatatransformationConfig:
     preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
          self.data_transformation_config = DatatransformationConfig()
          
    def get_data_transformation_object(self):
         try:
              logging.info('Initiating Data Transformation')
              ## categorical and numerical variables 
              categorical_cols = ['cut', 'color', 'clarity']
              numerical_cols = ['carat', 'depth', 'table', 'x', 'y', 'z']

              # Define the custom ranking for each ordinal variable
              cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
              color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
              clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

              logging.info('data tarsnformation pipeline initiated')

              ## Numerical Pipeline
              num_pipeline=Pipeline(
                        steps=[
                        ('imputer',SimpleImputer(strategy='median')),
                        ('scaler',StandardScaler())

                        ]

                 )

                    # Categorigal Pipeline
              cat_pipeline=Pipeline(
                        steps=[
                        ('imputer',SimpleImputer(strategy='most_frequent')),
                        ('ordinalencoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                        ('scaler',StandardScaler())
                        ]

                  )

              preprocessor=ColumnTransformer([
                    ('num_pipeline',num_pipeline,numerical_cols),
                    ('cat_pipeline',cat_pipeline,categorical_cols)
                    ]
                 )
              
              return preprocessor 
         
         
         except Exception as e:
               logging.info('exception occured in data transformation')
               raise CustomException(e,sys)
          
          
    def initiate_data_transformation(self,train_data_path,test_data_path):
         try:
              train_df = pd.read_csv(train_data_path)
              test_df = pd.read_csv(test_data_path)

              logging.info('read train and test data completed')
              logging.info(f'train dataframe head: \n {train_df.head().to_string()}')
              logging.info(f'test dataframe head: \n {test_df.head().to_string()}')
              
              preproessing_obj = self.get_data_transformation_object()
              target_column='price'
              drop_column = [target_column,'id']

              #dividing dataset to dependent and independent features
              #for tarin data
              input_feature_train_df = train_df.drop(columns=drop_column,axis=1)
              target_feature_train_df = train_df[target_column]
              #test data
              input_feature_test_df = test_df.drop(columns=drop_column,axis=1)
              target_feature_test_df = test_df[target_column]

              #data transformaation 
              input_feature_train_arr = preproessing_obj.fit_transform(input_feature_train_df)
              input_feature_test_arr = preproessing_obj.transform(input_feature_test_df)

              train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
              test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

              save_object(
                   file_path=self.data_transformation_config.preprocessor_obj_file_path,
                   obj = preproessing_obj
              )

              logging.info('applying preprocessing on train and test data completed')

              return(
                     train_arr,
                     test_arr,
                     self.data_transformation_config.preprocessor_obj_file_path
              )

              

         
         except Exception as e:
              raise CustomException(e,sys)