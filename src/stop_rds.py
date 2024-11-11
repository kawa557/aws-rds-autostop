import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    rds = boto3.client('rds')

    # Stop RDS
    db_instances = rds.describe_db_instances()
    for db_instance in db_instances['DBInstances']:
        db_instance_id = db_instance['DBInstanceIdentifier']
        tags = rds.list_tags_for_resource(ResourceName=db_instance['DBInstanceArn'])['TagList']
        for tag in tags:
            if tag['Key'] == 'shutdown' and tag['Value'] == 'true':
                rds.stop_db_instance(DBInstanceIdentifier=db_instance_id)
                logger.info(f'Stopped RDS instance: {db_instance_id}')