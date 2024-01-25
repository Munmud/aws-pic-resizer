import boto3
import logging
import os
import json


logger =  logging.getLogger('ImageSizeGetter')
logger.setLevel(logging.INFO)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE_NAME'))

def lambda_handler(event,context):

    logger.info(f"Reading event :\n {event} ")

    event = event[0]['body']
    event = json.loads(event)

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    response = table.scan()
    items = response.get('Items', [])

    res = {"ImageSize" : []}

    for item in items:
        res['ImageSize'].append({
            "Height": item['Height'],
            'Width':item['Width'],
            'bucket_name' : bucket_name,
            'file_key' : file_key
        })
    return res









