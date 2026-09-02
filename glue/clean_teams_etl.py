import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1787881247054 = glueContext.create_dynamic_frame.from_catalog(database="nba-pipeline-db", table_name="teams", transformation_ctx="AWSGlueDataCatalog_node1787881247054")

# Script generated for node SQL Query
SqlQuery0 = '''
SELECT
  team.id,
  team.conference,
  team.division,
  team.city,
  team.name,
  team.full_name,
  team.abbreviation
FROM myDataSource
LATERAL VIEW explode(data) exploded_table AS team
'''
SQLQuery_node1787881661691 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"myDataSource":AWSGlueDataCatalog_node1787881247054}, transformation_ctx = "SQLQuery_node1787881661691")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1787881661691, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1787878767423", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1787882336896 = glueContext.getSink(path="s3://zee-nba-pipeline-2026/processed/teams/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1787882336896")
AmazonS3_node1787882336896.setCatalogInfo(catalogDatabase="nba-pipeline-db",catalogTableName="teams_clean")
AmazonS3_node1787882336896.setFormat("glueparquet", compression="snappy")
AmazonS3_node1787882336896.writeFrame(SQLQuery_node1787881661691)
job.commit()
