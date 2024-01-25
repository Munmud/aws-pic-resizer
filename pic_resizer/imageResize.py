import boto3
import os
import logging
from io import BytesIO
from PIL import Image


s3 = boto3.client('s3')

logger =  logging.getLogger('PictureResize')
logger.setLevel(logging.INFO)

output_bucket_name = os.environ.get('S3_OUTPUT_BUCKET_NAME')

def resize_image(image_content, new_width, new_height):
    # Open the image using Pillow
    image = Image.open(BytesIO(image_content))

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    # Save the resized image to a BytesIO buffer
    output_buffer = BytesIO()
    resized_image.save(output_buffer, format="JPEG")
    resized_image_content = output_buffer.getvalue()

    return resized_image_content

def lambda_handler(event,context):
    logger.info(f"Reading event :\n {event} ")
    # logger.info(f"Reading output_bucket_name :\n {output_bucket_name} ")


    bucket_name = event['bucket_name']
    file_key = event['file_key']
    width = event['Width']
    height = event['Height']

    # # Download the image from S3
    response = s3.get_object(Bucket=bucket_name, Key = file_key)

    image_content = response['Body'].read()

    # # Resize the image
    resized_image = resize_image(image_content, new_width=width, new_height=height)

    # # Upload the resized image back to S3
    resized_key = f"resized/{str(width)}x{str(height)}/{os.path.basename(file_key)}"
    s3.put_object(Body=resized_image, Bucket=output_bucket_name, Key=resized_key)






