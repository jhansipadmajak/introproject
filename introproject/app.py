import json

# import requests
from datetime import datetime   
import pytz
import random
import boto3 
from boto3.dynamodb.conditions import Key
#client for DynamoDB
dynamodb = boto3.client('dynamodb')

def convert_time(timeline,event):
    local = pytz.timezone(timeline)
    naive = datetime.strptime(event['startAt'], "%d/%m/%y,%H:%M:%S")
    #naive = datetime.strptime(event, "%d/%m/%y,%H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    print(utc_dt)

def query_timeline(devId):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('test_device_table')
    print(table)
    response = table.query(
        KeyConditionExpression=Key('devid').eq('devId')
    )
    print(response['Items'][0]['devid'])
    #test return as i have no access to check on aws
    return 'America/Los_Angeles'
    
def lambda_handler(event, context):

    #personId = event['queryStringParameters']['personId']
    
    timeline=query_timeline(event['devId'])
    #"startAt": "21/09/23,18:00:00",
    utctime=convert_time(timeline,event)
   

    print(random.randint(0,600))
    event['startAt']=utctime
    event['interval'][-1]=event['interval'][-1]+random.randint(0,600)
    responseobj={"Body":event}
    responseobj.update({"Header":{"Authotization":12345}})
    print(responseobj)
    client = boto3.client('s3')
    client.put_object(Body=json.dumps(responseobj), Bucket='project-intro-bucket', Key=event['devId']+'.json')
    
    return {
        "statusCode": 200
    }
