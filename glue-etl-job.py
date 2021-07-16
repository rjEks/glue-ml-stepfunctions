import boto3

glue = boto3.client('glue')
glue_job_name = 'Job-Etl-Glue'
 
 
s3_script_path = 's3://bucket-name/gluescript/glue-etl-processing.py'
my_glue_role = 'GlueJobRole' # Nao esquecer de Criar a Role
 
 
response = glue.create_job(
    Name=glue_job_name,
    Description='Job de Dataprep para treinamento',
    Role=my_glue_role,
    ExecutionProperty={
        'MaxConcurrentRuns': 2
    },
    Command={
        'Name': 'glueetl',
        'ScriptLocation': s3_script_path,
        'PythonVersion': '3'
    },
    MaxRetries=2,
    Timeout=1440,
    Tags={
        'usecase': 'ml-workflow-preprocessing'
    },
    GlueVersion='1.0',
    NumberOfWorkers=5,
    WorkerType='Standard'
)
