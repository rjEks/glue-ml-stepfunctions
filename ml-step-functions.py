data_processing_step = GlueStartJobRunStep(
    state_id='GlueDataProcessingStep',
    parameters={
        'JobName': glue_job_name,
        'Arguments': {
            '--s3_input_data_path': 's3://bucket-name/medicare-dataset/',
            '--s3_processed_data_path': 's3://bucket-name/output'
        }
    }
)

xgb = sagemaker.estimator.Estimator(
    get_image_uri(region, 'xgboost'),
    sagemaker_execution_role,
    train_instance_count = 1,
    train_instance_type = 'ml.m4.4xlarge',
    train_volume_size = 5,
    output_path = f's3://bucket-name/output',
    sagemaker_session = session
)
 
xgb.set_hyperparameters(
    objective = 'reg:linear',
    num_round = 50,
    max_depth = 5,
    eta = 0.2,
    gamma = 4,
    min_child_weight = 6,
    subsample = 0.7   
)
 
training_step = TrainingStep(
    'TrainStep',
    estimator=xgb,
    data={
        'train': 's3://bucket-name/train',
        'validation': 's3://bucket-name/validation'
    },
    job_name='my-training-job-name' 
)

model_step = ModelStep(
    'SaveModel',
    model=training_step.get_expected_model(),
    model_name='sagemaer-xgb-model' 
)

# Configure SageMaker Batch Transform Step
transform_step = steps.TransformStep(
    'BatchPredictionStep',
    transformer=xgb.transformer(
        instance_count=1,
        instance_type='ml.m5.large'
    ),
    job_name='my-training-job-name',    
    model_name='my-sagemaker-model-name',
    data='s3://bucket-name/test',
    content_type='text/csv'
)

# Encadeando os steps
workflow_definition = Chain([
    data_processing_step,
    training_step,
    model_step,
    transform_step
])
 
 
workflow = Workflow(
    name='MyTrainTransformDeployWithGlue_v2',
    definition=workflow_definition,
    role=workflow_execution_role,
    execution_input=execution_input
)
 
workflow.render_graph()