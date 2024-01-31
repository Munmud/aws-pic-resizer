import boto3
import logging
import os
import json
import re


logger =  logging.getLogger('ImageSizeGetter')
logger.setLevel(logging.INFO)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE_NAME'))

def is_image_file(filepath):
    # Define a list of image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    # Get the file extension from the filepath
    _, file_extension = os.path.splitext(filepath)

    # Check if the file extension is in the list of image extensions
    return file_extension.lower() in image_extensions

def lambda_handler(event,context):

    # logger.info(f"Reading event :\n {event} ")
    res = {"ImageSize" : []}
    res['isImage'] = False

    event = json.loads(event[0]['body'])

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    isImage = is_image_file(file_key)

    pattern = r"Brand/(\d+)/Product/(\d+)/Variation/(\d+)/(.*?)$"
    match = re.match(pattern, file_key)

    if (isImage and match):
        res['isImage'] = True
        brand_id = match.group(1)
        product_id = match.group(2)
        variation_id = match.group(3)

        response = table.scan()
        items = response.get('Items', [])
        for item in items:
            res['ImageSize'].append({
                "Height": item['Height'],
                'Width':item['Width'],
                'bucket_name' : bucket_name,
                'file_key' : file_key,
                'brand_id': brand_id,
                'product_id' : product_id,
                'variation_id' : variation_id
            })
    return res













