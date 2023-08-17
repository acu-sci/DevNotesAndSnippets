This folder contains the following:
1. sagemaker_lambda_layer: zip file to upload with the lambda layer definition. The Lambda functions that create the pipelines need this layer to have access to the sagemaker library  
    - To create your own zip file for a lambda layer you need:  
        * mkdir folder  
        * cd folder  
        * virtualenv v-env -p python3.x -> depending on which is your python version  
        * source ./v-env/bin/activate  
        * pip install pandas -> or in this case sagemaker  
        * deactivate  
        * mkdir python  
        * cd python  
        * cp -r ../venv/lib/python3.x/site-packages/* .   
        * cd ..  
        * zip -r pandas_layer.zip python  
   
    This file is then uploaded when creating the lambda layer.  

2. train_lightgbm_pipeline_lambda.py -> python file to be executed by the lambda function in order to define and register the training pipeline in the project's sagemaker.  
The lambda should have a custom IAM-Role that has the necessary lambda, sagemaker and s3 permissions to access all necessary resources and register the pipeline.  
This pipeline is executed whenever the model needs retraining.
3. predict_lightgbm_pipeline_lambda.py -> python file to be executed by the lambda function in order to define a register the prediction pipeline  
    The function runs with the same custom IAM. One Role is enough for all lambdas that define sagemaker pipelines.
    An Eventbridge rule can execute this pipeline whenever it is necessary. For example, the evaluation pipeline might run daily to make predictions with the new data from the previos day.
4. sourcedir tarball for evaluation: To be uploaded in the sagemaker processing step that executes the lightgbm model evaluation  
    - The tarball contains a folder with the following structure:  
        * /constants  
        * /lib -> containing the wheels of all necessary packages  
        * __init__.py  
        * abalone_evaluation.py  
        * requierments.txt -> should point to the wheels in lib !   whatch out for the absolute path!
        * script_requierements.txt  
        * version  
    To create this tarball I downloaded the tarball provided by aws for lightgbm and added the abalone_evaluation.py script to the directory:
    public available s3: jumpstart-cache-prod-eu-west-1/source-directory-tarballs/lightgbm/inference/regression/v1.2.0/sourcedir.tar.gz  
    The tarball has to be always called **sourcedir.tar**.gz otherwise the processing or inference step wont understand what it is
5. sourcedir tarball for inference: To be uploaded in the transform step that generates predictions with the trained lightgbm model  
    - This is the same downloaded tarball but copied in an won s3 so that the pipeline has write access on it (otherwise it will throw an error)  
        *  /constants
        * /lib -> containing the wheels of all necessary packages
        * __init__.py
        * inference.py
        * requierments.txt -> should point to the wheels in lib ! whatch out for the absolute path!
        * script_requierements.txt
        * version


Comments:
- This are 2 pipelines customed to train and predict with a model based on lightgbm. A different algorithm would requiere a different customization of the steps.
For an example with XGBoost see: 
https://docs.aws.amazon.com/sagemaker/latest/dg/define-pipeline.html
Fully suported algotithms (like XGBoost) require much less customization and management

- Right now python scripts to execute within the pipeline are passed to the steps with an s3-adresss,
It would be better if the project's CICD takes care of uploading this files together with the lambda handler. This scripts can then be referenced in the lambda handler using the local path.  

- Pipelines can be executed in the following ways:
    from a python script: e.g. lambda
    with an EventBridge rule: EventBridge has direct integration with sagemaker pipelines. An event or a schedule can start a pipeline execution
    manuelly from sagemaker studio

- Looks like pipelines can only be deleted from a python script (probably also with aws cli)