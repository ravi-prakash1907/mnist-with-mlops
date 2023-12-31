import datetime as dt

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from model import mnist_model
from core.process.abstract_process import abstract_process

class process(abstract_process):

    def __init__(self):
        # Declare Default arguments for the DAG
        default_args = {
            'owner': 'princ3',
            'depends_on_past': False,
            'start_date': dt.datetime.strptime('2020-09-24T00:00:00', '%Y-%m-%dT%H:%M:%S'),
            'provide_context': True
        }

        # creating a new dag
        self.dag = DAG('mnist_process_dag', default_args=default_args, schedule_interval='@daily', max_active_runs=1)

    def get_operator(self,func,task_id):
        return PythonOperator(task_id=task_id, python_callable=func,op_kwargs={}, dag=self.dag)

    def log_model(self):
        pass

    def serve_model(self):
        pass

    def get_dag(self):

        model = mnist_model()
        load_data = self.get_operator(model.load_data, 'load_data')
        prep_data = self.get_operator(model.prep_data, 'prep_data')
        build_model = self.get_operator(model.build_model, 'build_model')
        train_model = self.get_operator(model.train_model, 'train_model')
        test_model = self.get_operator(model.test_model, 'test_model')
        log_model = self.get_operator(model.log_model, 'log_model')
        serve_model = self.get_operator(model.serve_model, 'serve_model')

        # setting process flow
        load_data>>prep_data>>build_model>>train_model>>test_model>>log_model>>serve_model

        return self.dag


