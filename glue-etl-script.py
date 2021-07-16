#Obtendo dado de entrada
  
import sys

from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
s3_input_data_path = 's3://bucket-name/medicare-dataset/'

input_df = spark.read.load(s3_input_data_path, format="csv", inferSchema=True, header=False)

# split treino e validacao
splits = input_df.randomSplit([0.5, 0.3, 0.2], 0)
print("Split dos dados em treino  validacao e teste")
 
train_df = splits[0]
validation_df = splits[1]
test_df = splits[2]

train_data_output_path = f's3://bucket-name/train'
validation_data_output_path = f's3://bucket-name/validation'
test_data_output_path = f's3://bucket-name/test'
 
print(f"Dados treino - output path: {train_data_output_path}")
print(f"Dados de validacao - output path: {validation_data_output_path}")
print(f"Dados de teste - output path: {test_data_output_path}")
 
# escrevendo arquivos no s3
train_df.coalesce(1).write.csv(train_data_output_path, mode='overwrite', header=False)
validation_df.coalesce(1).write.csv(validation_data_output_path, mode='overwrite', header=False)
test_df.coalesce(1).write.csv(test_data_output_path, mode='overwrite', header=False)
