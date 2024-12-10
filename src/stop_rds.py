import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
rds = boto3.client('rds')

def handler(event, context):
    # Stop DB instances
    dbs = rds.describe_db_instances()
    for db in dbs['DBInstances']:
        # Check if DB instance is not already stopped
        if db['DBInstanceStatus'] == 'available':
            try:
                GetTags = rds.list_tags_for_resource(ResourceName=db['DBInstanceArn'])['TagList']
                for tags in GetTags:
                    # if tag "shutdown=true" is set for instance, stop it
                    if tags['Key'] == 'shutdown' and tags['Value'] == 'true':
                        result = rds.stop_db_instance(DBInstanceIdentifier=db['DBInstanceIdentifier'])
                        logger.info("Stopping instance: {0}.".format(db['DBInstanceIdentifier']))
            except Exception as e:
                logger.error("Cannot stop instance {0}.".format(db['DBInstanceIdentifier']))
                logger.error(e)

    # Stop DB clusters
    clusters = rds.describe_db_clusters()
    for cluster in clusters['DBClusters']:
        # Check if DB cluster is not already stopped
        if cluster['Status'] == 'available':
            try:
                GetTags = rds.list_tags_for_resource(ResourceName=cluster['DBClusterArn'])['TagList']
                for tags in GetTags:
                    # if tag "shutdown=true" is set for cluster, stop it
                    if tags['Key'] == 'shutdown' and tags['Value'] == 'true':
                        result = rds.stop_db_cluster(DBClusterIdentifier=cluster['DBClusterIdentifier'])
                        logger.info("Stopping cluster: {0}.".format(cluster['DBClusterIdentifier']))
            except Exception as e:
                logger.error("Cannot stop cluster {0}.".format(cluster['DBClusterIdentifier']))
                logger.error(e)