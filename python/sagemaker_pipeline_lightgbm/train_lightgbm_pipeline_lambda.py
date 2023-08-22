# The lambda function that executes this script should have attached a lambda layer with the sagemaker package

import json
import boto3
import sagemaker
from sagemaker.workflow.parameters import ParameterInteger, ParameterString
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.steps import ProcessingStep, TrainingStep, CacheConfig
from sagemaker.workflow.pipeline import Pipeline
#from sagemaker.workflow.pipeline import PipelineExperimentConfig
from sagemaker.workflow.pipeline_context import PipelineSession

from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.sklearn import SKLearn
from sagemaker.processing import FrameworkProcessor, ProcessingInput, ProcessingOutput
from sagemaker import image_uris, model_uris, script_uris
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput

from sagemaker.workflow.model_step import ModelStep
from sagemaker import Model
from sagemaker.model_metrics import MetricsSource, ModelMetrics

#from smexperiments.experiment import Experiment

def lambda_handler(event, context):
    
    aws_region = boto3.Session().region_name
    # if the script gets executed by the ci/cd the same role will be taken to execute this script and needs to be granted permissions to sagemaker ressources
    aws_role = sagemaker.get_execution_role()
    # define a bucket to store pipeline objects 
    default_bucket = "sagemaker-eu-west-123456789"
    
    # Start a Pipeline Session to create all sagemaker pipeline resources
    pipeline_session = PipelineSession()
    
    model_package_group_name = "PipelineTestModel"
    # does the experiment name need to change every time?
    #experiment_name = "PipelineTestTraining"
    pipeline_name = "PipelineTestTraining"
    base_job = "pipeline-training"
    
    # steps
    # define where the scripts are
    # first solve it through files published in a bucket, then think about how to implement it better
    step_feature_engineering_name = "PipelineTestFeatureEngineeringStep"
    step_training_name = "PipelineTestTrainingStep"
    step_eval_name = "PipelineTestEvaluationStep"
    step_create_name = "PipelineTestCreateModel"
    step_register_model_name = "PipelineTestRegisterModel"
    
    # define key for path where model object will be stored
    model_bucket_key = f"{default_bucket}/{pipeline_name}/{base_job}/pipeline-test"
    # model storage path
    model_path = f"s3://{model_bucket_key}"
    
    # Cache Pipeline steps to reduce execution time on subsequent executions
    cache_config = CacheConfig(enable_caching=True, expire_after="15m")
    
    # Training time timeout
    timeout_sec = 600
    
    '''
        THIS EXAMPLE IS BASED ON THE ABALONE DATA. I DOWNLOADED THIS DATA AS A CSV FILE
        AND UPLOADED IT TO A S3 BUCKET AVAILABLE TO THE PIPELINE.
        TO PUT THIS PIPELINE IN PRODUCTION ATTACH THE CORRECT DATASOURCE AS
        AN INPUT_DATA PIPELINE OBJECT
    '''
    # path in sagemaker instance to upload the data to the pipeline's bucket
    # with this pipeline parameter you can pass on the adress of the input csv data
    input_data_uri = f"s3://{default_bucket}/pipeline_test_abalone_data/abalone-dataset.csv"
    
    # define pipeline arameters as pipeline objects
    processing_instance_count = ParameterInteger(
        name="ProcessingInstanceCount",
        default_value=1
    )
    training_instance_count = ParameterInteger(
        name="trainingInstanceCount",
        default_value=1
    )
    eval_instance_count = ParameterInteger(
        name="EvaluationInstanceCount",
        default_value=1
    )
    model_approval_status = ParameterString(
        name="ModelApprovalStatus",
        default_value="PendingManualApproval"
    )
    input_data = ParameterString(
        name="InputData",
        default_value=input_data_uri,
    )

    '''
    installing the sagemaker-experiments in lambda might be too complicated and not woth it for what it offers
    # create an experiment if it doesnt exist
    try:
        pipeline_experiment = Experiment.load(experiment_name=experiment_name)
        print("existing experiment loaded")
    except Exception as ex:
        if "ResourceNotFound" in str(ex):
            pipeline_experiment = Experiment.create(
                experiment_name=experiment_name,
                description=f"Experiment containing Sagemaker Pipeline: {pipeline_name}",
            )
            print("new experiment created")
        else:
            print(f"Unexpected {ex}, {type(ex)}")
            print("Dont go forward!")
            raise
    
    '''
    
    
    '''
    won't be using the trials as I want to create the produtive pipeline to get executed anytime e.g. from eventbridge events
    
    create_date = strftime("%Y-%m-%d-%H-%M-%S")
    # create trial for the pipeline execution
    demo_trial = Trial.create(
        trial_name=f'{experiment_name}-{create_date}',
        experiment_name=pipeline_experiment.experiment_name,
        tags=[{'Key': 'demo-trials-sagemaker-pipelines', 'Value': 'demo1-retabalone'}]
    )
    
    '''
    
    ####################### preprocessing #################################
    # define processor for feature engineering job
    # use a simple image from the ones avaibale in AWS.
    # This preprocessing script uses a sklearn pipeline. All needed packages are
    # installed in the defined image
    framework_version = "0.23-1"
    
    sklearn_processor = SKLearnProcessor(
        role=aws_role,
        sagemaker_session=pipeline_session,
        framework_version=framework_version,
        instance_type="ml.m5.xlarge",
        instance_count=processing_instance_count,
        base_job_name=f"{base_job}/feature-engineering" 
    )
    
    # define step with inputs and outputs
    step_feature_engineering = ProcessingStep(
        name=step_feature_engineering_name,
        processor=sklearn_processor,
        inputs=[
            ProcessingInput(source=input_data, destination="/opt/ml/processing/input"),  
        ],
        outputs=[
            ProcessingOutput(output_name="training", source="/opt/ml/processing/output"),
            ProcessingOutput(output_name="train", source="/opt/ml/processing/train"),
            ProcessingOutput(output_name="validation", source="/opt/ml/processing/validation"),
            ProcessingOutput(output_name="test", source="/opt/ml/processing/test")
        ],
        # the script is also uploaded to the standard sagemaker bucket
        code=f"s3://{default_bucket}/pipeline_test_scripts/scripts_abalone/abalone_preprocessing.py",
    )
    
    ####################### training #################################
    
    # define training image and model parameters
    train_model_id, train_model_version, train_scope = "lightgbm-regression-model", "*", "training"
    
    # Retrieve the docker image
    train_image_uri = image_uris.retrieve(
        region=None,
        framework=None,
        model_id=train_model_id,
        model_version=train_model_version,
        image_scope=train_scope,
        instance_type="ml.m5.xlarge",
    )
    # Retrieve the training script
    train_source_uri = script_uris.retrieve(
        model_id=train_model_id, model_version=train_model_version, script_scope=train_scope
    )
    # Retrieve the pre-trained model tarball to further fine-tune
    train_model_uri = model_uris.retrieve(
        model_id=train_model_id, model_version=train_model_version, model_scope=train_scope
    )
    
    # Define hyperparameters for lightgbm
    hyperp_lightgbm = {
        'num_boost_round': '500',
        'early_stopping_rounds': '30',
        'metric': 'auto',
        'learning_rate': '0.009',
        'num_leaves': '67',
        'feature_fraction': '0.74',
        'bagging_fraction': '0.53',
        'bagging_freq': '5',
        'max_depth': '11',
        'min_data_in_leaf': '26',
        'max_delta_step': '0.0',
        'lambda_l1': '0.0',
        'lambda_l2': '0.0',
        'boosting': 'gbdt',
        'min_gain_to_split': '0.0',
        'tree_learner': 'serial',
        'feature_fraction_bynode': '1.0',
        'is_unbalance': 'False',
        'max_bin': '255',
        'tweedie_variance_power': '1.5',
        'num_threads': '0',
        'verbosity': '1'
    }
    
    # Create SageMaker Estimator instance
    lightgbm = Estimator(
        role=aws_role,
        sagemaker_session=pipeline_session,
        image_uri=train_image_uri,
        source_dir=train_source_uri,
        model_uri=train_model_uri,
        entry_point="transfer_learning.py",
        instance_count=training_instance_count,
        instance_type="ml.m5.xlarge",
        max_run=timeout_sec,
        hyperparameters=hyperp_lightgbm,
        output_path=model_path,
        enable_sagemaker_metrics=True,
        metric_definitions=[
            {"Name": "rmse", "Regex": "rmse: ([0-9\\.]+)"},
            {"Name": "l1", "Regex": "l1: ([0-9\\.]+)"},
            {"Name": "l2", "Regex": "l2: ([0-9\\.]+)"},
        ],
        base_job_name=f"{base_job}/model-training" 
    )
    
    
    # define tuning step
    # define training step
    step_train = TrainingStep(
        name=step_training_name,
        estimator=lightgbm,
        inputs={
            "training": TrainingInput(
                s3_data=step_feature_engineering.properties.ProcessingOutputConfig.Outputs[
                    "training"
                ].S3Output.S3Uri
            )
        },
    )
    
    ####################### evaluating #################################
    
    # define processor image to use for evaluating model metrics
    # define inference image and model parameters
    eval_model_id, eval_model_version, eval_scope = "lightgbm-regression-model", "*", "inference"
    
    # Retrieve the docker image for eval
    image_uri_eval = image_uris.retrieve(
        region=None,
        framework=None,
        model_id=eval_model_id,
        model_version=eval_model_version,
        image_scope=eval_scope,
        instance_type="ml.m5.xlarge",
    )

    # Retrieve the inference script
    # the downloaded source not only contains the inference.py script, but also the libraries needed to run it:
    # Including LightGBM itself! The Package is not loaded with the image but with the source!
    # If you don't pass such a script you wont be able tu use lightGBM
    eval_source_uri = script_uris.retrieve(
        model_id=eval_model_id, model_version=eval_model_version, script_scope=eval_scope
    )
    
    # deploying an entrypoint just to do the evaluation seems like too much looping around
    # try to pass the lightgbm package the same way the training script does it
    
    # The class ScriptProcessor doesn't support submitting an own source directory.
    # since the image used by AWS to support LightGBM doesn't come with LightGBM installed,
    # we need the ability to submit a source_dir that gets installed in the container
    # Framework Processors have this capability when used together with the .run() method and a pipeline session

    script_eval = FrameworkProcessor(
        role=aws_role,
        sagemaker_session=pipeline_session,
        estimator_cls=SKLearn,
        framework_version='0.23-1',
        instance_count=eval_instance_count,
        image_uri=image_uri_eval,
        instance_type='ml.m5.large',
    )

    # write output to evaluation.json file
    evaluation_report = PropertyFile(
        name="EvaluationReport",
        output_name="evaluation",
        path="evaluation.json"
    )

    # Pass runtime parameters to the ProcessorStep
    # TODO: Check how to optimize this workaround with the sourcedir to make LightGBM available to the script
    eval_step_args = script_eval.run(
        source_dir=f"s3://{default_bucket}/pipeline_test_scripts/scripts_abalone/evaluation/sourcedir.tar.gz",
        code="abalone_evaluation.py",
        inputs=[
            ProcessingInput(
                source=step_train.properties.ModelArtifacts.S3ModelArtifacts,
                destination="/opt/ml/processing/model"
            ),
            ProcessingInput(
                source=step_feature_engineering.properties.ProcessingOutputConfig.Outputs[
                    "test"
                ].S3Output.S3Uri,
                destination="/opt/ml/processing/test"
            )
        ],
        outputs=[
            ProcessingOutput(output_name="evaluation", source="/opt/ml/processing/evaluation"),
        ]
    )
    
    # define evaluation step
    step_eval = ProcessingStep(
        name=step_eval_name,
        step_args=eval_step_args,
        property_files=[evaluation_report],
    )
    
    ####################### register model #################################
    
    # define inference image and model parameters
    inference_model_id, inference_model_version, inference_scope = "lightgbm-regression-model", "*", "inference"
    
    # Retrieve the docker image for inference
    inference_image_uri = image_uris.retrieve(
        region=None,
        framework=None,
        model_id=inference_model_id,
        model_version=inference_model_version,
        image_scope=inference_scope,
        instance_type="ml.m5.xlarge",
    )
    # Retrieve the inferenceing script and source dir
    inference_source_uri = script_uris.retrieve(
        model_id=inference_model_id, model_version=inference_model_version, script_scope=inference_scope
    )
    
    # TODO: Check how to optimize this workaround with the sourcedir to make LightGBM available to the script
    trained_model = Model(
        role=aws_role,
        sagemaker_session=pipeline_session,
        image_uri=inference_image_uri,
        source_dir=f"s3://{default_bucket}/pipeline_test_scripts/scripts_abalone/inference/sourcedir.tar.gz",
        entry_point="inference.py",
        model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts
    )
    
    model_metrics = ModelMetrics(
        model_statistics=MetricsSource(
            s3_uri="{}/evaluation.json".format(
                step_eval.arguments["ProcessingOutputConfig"]["Outputs"][0]["S3Output"]["S3Uri"]
            ),
            content_type="application/json",
        )
    )
    
    register_args = trained_model.register(
        content_types=["text/csv"],
        response_types=["text/csv"],
        inference_instances=["ml.t2.medium", "ml.m5.xlarge"],
        transform_instances=["ml.m5.xlarge"],
        model_package_group_name=model_package_group_name,
        approval_status=model_approval_status,
        model_metrics=model_metrics
    )
    
    
    step_register_model = ModelStep(name=step_register_model_name, step_args=register_args)
    
    #pipeline_experiment_config = PipelineExperimentConfig(
    #    pipeline_experiment.experiment_name,
    #    ExecutionVariables.PIPELINE_EXECUTION_ID
    #)
    
    # pass on the pipeline execition role here
    pipeline = Pipeline(
        name=pipeline_name,
        #pipeline_experiment_config=pipeline_experiment_config,
        sagemaker_session=pipeline_session,
        parameters=[
            processing_instance_count,
            training_instance_count,
            eval_instance_count,
            model_approval_status,
            input_data
        ],
        steps=[step_feature_engineering, step_train, step_eval, step_register_model]
    )


    # submit pipeline definition
    pipeline.upsert(role_arn=aws_role)