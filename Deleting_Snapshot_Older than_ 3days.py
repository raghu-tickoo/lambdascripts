import json
import boto3
from pprint import pprint
from datetime import datetime, timezone
def lambda_handler(event, context):
    ec2client = boto3.client('ec2')
    ec2resource=boto3.resource('ec2')
          ##Finding the Region
    locations = [region['RegionName'] for region in ec2client.describe_regions()['Regions']]
    for region in locations:
        ec2resource = boto3.resource('ec2', region_name=region)
        print("Region is", region)
        instances = ec2resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    for instance in instances:
        #describing the snapshot
        snapshot_response = ec2client.describe_snapshots(OwnerIds=['self'])
        for snapshot in snapshot_response['Snapshots']:
            #details involved with the snapshot
            print(snapshot['SnapshotId'])
            print(snapshot['VolumeId'])
            print(snapshot['VolumeSize'], "GB")
            print(snapshot['StartTime'])
            #process to delete the snapshot which is older than three days
            days_old = days_old = (datetime.now(timezone.utc) - snapshot['StartTime']).days
            print(days_old)
            if (days_old>3):
                print("The snapshot", snapshot['SnapshotId'], "is older than three days and will be deleted" )
                ec2client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            else:
                print("The snapshot is not older than three days , and will not be deleted" )

    
     
