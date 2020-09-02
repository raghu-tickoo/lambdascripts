import json
import boto3
from pprint import pprint
def lambda_handler(event, context):
    ec2client=boto3.client('ec2')
    locations=ec2client.describe_regions()
    list_of_regions=[]
             #Placing the regions in the list, called list of regions
    for each_region in locations['Regions']:
        list_of_regions.append(each_region['RegionName'])
             # Iterating over each region
        for each_region in list_of_regions:
            ec2resource = boto3.resource('ec2', region_name=each_region)
            print("Region is", each_region)
            instances = ec2resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
             #Stop the instances 
            for instance in instances:
                instance.stop()
                print('stopped instance:', instance.id)
