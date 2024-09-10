import boto3

def lambda_handler(event, context):
    rds = boto3.client('rds')
    # 全RDSインスタンスを取得
    instances = rds.describe_db_instances()
    instance_ids = []

    for instance in instances['DBInstances']:
        # タグを確認
        tags = rds.list_tags_for_resource(ResourceName=instance['DBInstanceArn'])
        tag_dict = {tag['Key']: tag['Value'] for tag in tags['TagList']}
        if tag_dict.get('auto_shutdown') == 'true':
            instance_ids.append(instance['DBInstanceIdentifier'])
    
    if instance_ids:
        for instance_id in instance_ids:
            rds.stop_db_instance(DBInstanceIdentifier=instance_id)
        print(f'Stopped your RDS instances: {instance_ids}')
    else:
        print('No RDS instances to stop')