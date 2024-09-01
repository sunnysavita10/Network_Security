from asyncio import tasks
import json
from textwrap import dedent
import pendulum
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
load_dotenv()


with DAG(
    'network_prediction',
    default_args={'retries': 2},
    # [END default_args]
    description='Network Security Prediction',
    schedule_interval="@weekly",
    start_date=pendulum.datetime(2024, 9, 1, tz="UTC"),
    catchup=False,
    tags=['example'],
) as dag:

    
    def download_files(**kwargs):
        bucket_name = "my-network-datasource"
        input_dir = "/app/input_files"
        #creating directory
        os.makedirs(input_dir,exist_ok=True)
        os.system(f"aws s3 sync s3://{bucket_name}/input_files /app/input_files")

    def batch_prediction(**kwargs):
        from networksecurity.pipeline.batch_prediction import start_batch_prediction
        input_dir = "/app/input_files"
        for file_name in os.listdir(input_dir):
            #make prediction
            start_batch_prediction(input_file_path=os.path.join(input_dir,file_name))
    
    def sync_prediction_dir_to_s3_bucket(**kwargs):
        bucket_name = "my-network-datasource"
        #upload prediction folder to predictionfiles folder in s3 bucket
        os.system(f"aws s3 sync /app/prediction s3://{bucket_name}/prediction_files")
    

    download_input_files  = PythonOperator(
            task_id="download_file",
            python_callable=download_files

    )

    generate_prediction_files = PythonOperator(
            task_id="prediction",
            python_callable=batch_prediction

    )

    upload_prediction_files = PythonOperator(
            task_id="upload_prediction_files",
            python_callable=sync_prediction_dir_to_s3_bucket

    )

    download_input_files >> generate_prediction_files >> upload_prediction_files