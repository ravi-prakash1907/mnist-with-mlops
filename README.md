# mnist

## Installation
- Create Virtual Environment
    - `sudo apt-get update -y`
    - `sudo apt-get upgrade`
    - `sudo apt-get install -y python3-venv`
    - `mkdir -p ~/envs`
    - `cd ~/envs`
    - `python3 -m venv mlops`

- Activate Virtual Environment
    - `. ~/envs/mlops/bin/activate`

- Install Dependencies
    - `pip install -r requirements.txt`
    
- Configure Airflow
    - `nano ~/airflow/airflow.cfg`
        - `dags_folder = /mnist/src` (src folder in the current directory)

- Setting up the executable:  
    - `chmod +x init` (granting permission to execute)  

## Execution

- Activate the virtual environment  
    - `. ~/envs/mlops/bin/activate`  

- Run the project  
    - `sh ./init`  

Open following links in browser:  
> Airflow UI: [http://0.0.0.0:8080/#/](http://0.0.0.0:8080/#/)  
> MLFlow UI: [http://0.0.0.0:5000/#/](http://0.0.0.0:5000/#/)
