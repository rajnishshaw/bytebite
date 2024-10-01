# import modules

import boto3
import json
import base64
import os


# create bedrock object
bedrock = boto3.client(service_name='bedrock-runtime')
# s3 bucket name
s3_bucket = os.environ['S3_BUCKET_NAME']
# Bedrock model id
bedrock_model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'

# process s3 object
def process_image(source_img):
    s3 = boto3.client('s3')
    lambda_img_location = '/tmp/'+ source_img.split('/')[-1]
    response = s3.download_file(s3_bucket, source_img, lambda_img_location)
    with open(lambda_img_location, 'rb') as image:
        base64_image = base64.b64encode(image.read()).decode('utf-8')
    return base64_image
    

# Claude-3 model body
def model_body(base64_image, media_type, input_query):
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/" + media_type,
                                "data": base64_image
                                }

                            },
                        {
                            "type": "text",
                            "text": input_query
                        }
                    ]
                }
            ]
        }
    )
    return body

# Bedrock inference function

def ask_bedrock(bedrock_model_id, model_body):
    try:
        response = bedrock.invoke_model(
            modelId=bedrock_model_id,
            body= model_body
            )
        response_body = json.loads(response['body'].read().decode('utf-8'))
        response_data = response_body['content'][0]['text']
        return response_data
    except:
        return None

def lambda_handler(event, context):
    source_img = event['queryStringParameters']['source_img']
    input_query = event['queryStringParameters']['input_query']
    media_type = source_img.split('/')[-1].split('.')[-1].lower()
    
    # convert image to base64
    base64_image = process_image(source_img)
    
    body = model_body(base64_image, media_type, input_query)
    
    response = ask_bedrock(bedrock_model_id, body)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
        
    }
    