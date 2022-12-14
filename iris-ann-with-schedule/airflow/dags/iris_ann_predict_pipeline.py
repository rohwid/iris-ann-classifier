import os
import json
import copy
import requests

from pathlib import Path
from datetime import datetime, timedelta

from airflow import DAG

from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.hooks.postgres_hook import PostgresHook

from iris_ann_predict_helper import helper


# PROJECT NAME
project_config = Variable.get('iris_ann_predict', deserialize_json=True)
PIPELINE_NAME = project_config['pipeline_name']
PROJECT = project_config['project']

# INPUT DATA
data_config = Variable.get('iris_ann_predict', deserialize_json=True)
INPUT_DATA = data_config['input_data']

# DB
db_config = Variable.get('iris_ann_predict', deserialize_json=True)
DB_URI = db_config['db_uri']

# INPUT TABLE
input_database_config = Variable.get('iris_ann_predict', deserialize_json=True)
INPUT_TABLE_NAME = input_database_config['input_table']
INPUT_COLUMN = input_database_config['input_column']

# OUTPUT TABLE
output_database_config = Variable.get('iris_ann_predict', deserialize_json=True)
OUTPUT_TABLE_NAME = output_database_config['output_table']
OUTPUT_COLUMN = output_database_config['output_column']

# IRIS_ANN ENDPOINT
endpoint_config = Variable.get('iris_ann_predict', deserialize_json=True)
API_ENDPOINT = endpoint_config['iris_ann_api']

# AIRFLOW CONNECTION
conn_config = Variable.get('iris_ann_predict', deserialize_json=True)
CONN_DB = conn_config['conn_db']


default_args = {
    'owner': 'Rohman',
    'start_date': datetime(2022, 9, 25, 0),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

# is_input_table_empty
def check_input_table():
    request = f'SELECT * FROM {INPUT_TABLE_NAME}'
    
    postgres_hook = PostgresHook(postgres_conn_id=CONN_DB)
    
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    
    try:
        cursor.execute(request)
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if not result:
            return 'insert_input_data_if_exist'

        return 'predict_with_data_from_db'
    except Exception as err:
        print(err)
        cursor.close()
        connection.close()


# insert_input_data_if_exist
def check_and_insert_input_data():
    new_file = Path(INPUT_DATA)

    if new_file.is_file():
        try:
            helper.insert_tb_input(DB_URI, INPUT_TABLE_NAME, INPUT_DATA)
            os.remove(INPUT_DATA)

            return 'predict_with_init_data'
        except Exception as err:
            return (err)
    
    return 'error_empy_init_data'
    

# predict_with_init_data, predict_with_data_from_db
def predict_and_insert_output_data():
    new_file = Path(INPUT_DATA)

    if new_file.is_file():
        try:
            helper.insert_tb_input(DB_URI, INPUT_TABLE_NAME, INPUT_DATA)
            os.remove(INPUT_DATA)
        except Exception as err:
            return (err)

    data = helper.query_all_tb_input(DB_URI, INPUT_TABLE_NAME)
    data_wo_ids = copy.deepcopy(data)

    for data_wo_id in data_wo_ids:
        del data_wo_id['id']

    try:
        response = requests.post(API_ENDPOINT, json=data_wo_ids)
        dict_response = json.loads(response.text)
        results = dict_response['response']

        for i in range(len(results)):
            temp_class = results[i]
            results[i] = {
                'executed_at': helper.generate_date_timestamp(),
                'id': int(data[i]['id']),
                'classes': int(temp_class)
            }

        helper.insert_tb_output(DB_URI, OUTPUT_TABLE_NAME, results)
    except Exception as err:
        print(err)


with DAG(dag_id = PIPELINE_NAME, 
         schedule_interval = "0 3 * * *",
         default_args = default_args, 
         catchup = False) as dag:

    create_input_table_if_not_exist = PostgresOperator(
        task_id ='create_input_table_if_not_exist',
        postgres_conn_id = CONN_DB,
        sql = f"""
            CREATE TABLE IF NOT EXISTS %s (
                %s SERIAL PRIMARY KEY, 
                %s FLOAT NOT NULL, 
                %s FLOAT NOT NULL, 
                %s FLOAT NOT NULL, 
                %s FLOAT NOT NULL
            );
        """ % (
            INPUT_TABLE_NAME,
            INPUT_COLUMN[0],
            INPUT_COLUMN[1],
            INPUT_COLUMN[2],
            INPUT_COLUMN[3],
            INPUT_COLUMN[4]
        )
    )

    create_output_table_if_not_exist = PostgresOperator(
        task_id ='create_output_table_if_not_exist',
        postgres_conn_id = CONN_DB,
        sql = f"""
            CREATE TABLE IF NOT EXISTS %s (
                %s TIMESTAMPTZ NOT NULL, 
                %s INT NOT NULL, 
                %s INT NOT NULL
            );
        """ % (
            OUTPUT_TABLE_NAME,
            OUTPUT_COLUMN[0],
            OUTPUT_COLUMN[1],
            OUTPUT_COLUMN[2]
        )
    )

    is_input_table_empty = BranchPythonOperator(
        task_id='is_input_table_empty',
        python_callable=check_input_table,
        dag = dag
    )

    insert_input_data_if_exist = BranchPythonOperator(
        task_id = 'insert_input_data_if_exist',
        python_callable = check_and_insert_input_data,
        dag = dag
    )

    predict_with_init_data = PythonOperator(
        task_id = 'predict_with_init_data',
        python_callable = predict_and_insert_output_data,
        dag = dag
    )

    error_empy_init_data = BashOperator(
        task_id = 'error_empy_init_data',
        bash_command = f"""
            echo "NO DATA! Please create 'new-iris-data.csv' and put it in '/opt/airflow/data' directory."
            echo "Here is the example data of \"new-iris-data.csv\" file:"
            echo ""
            echo "sepal_length,sepal_width,petal_length,petal_width"
            echo "5.1,3.5,1.4,0.2"
            echo "5.1,3.5,1.4,0.2"
            echo ""
            echo "You can copy that and save as 'new-iris-data.csv' file."
        """
    )

    predict_with_data_from_db = PythonOperator(
        task_id = 'predict_with_data_from_db',
        python_callable = predict_and_insert_output_data,
        dag = dag
    )


    # init data
    task_1 = (create_input_table_if_not_exist >> create_output_table_if_not_exist >> 
              is_input_table_empty >> [insert_input_data_if_exist, predict_with_data_from_db])
    task_2 = (create_input_table_if_not_exist >> create_output_table_if_not_exist >> 
              is_input_table_empty >> insert_input_data_if_exist>> [predict_with_init_data, error_empy_init_data])
    task_3 = (create_input_table_if_not_exist >> create_output_table_if_not_exist >> 
              is_input_table_empty >> insert_input_data_if_exist>> predict_with_init_data)
    task_4 = (create_input_table_if_not_exist >> create_output_table_if_not_exist >> 
              is_input_table_empty >> insert_input_data_if_exist>> error_empy_init_data)

    # db is not empty
    task_5 = (create_input_table_if_not_exist >> create_output_table_if_not_exist >> 
              is_input_table_empty >> predict_with_data_from_db)
