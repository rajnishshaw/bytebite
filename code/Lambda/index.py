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
#bedrock_model_id = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
#bedrock_model_id = 'anthropic.claude-3-opus-20240229-v1:0'
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
def model_body(input_query, base64_image=None, media_type=None):
    content = [
        {
            "type": "text",
            "text": input_query
        }
    ]
    
    if base64_image and media_type:
        content.insert(0, {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": f"image/{media_type}",
                "data": base64_image
            }
        })
    
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "user",
                    "content": content
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
    input_query = event['queryStringParameters']['input_query']
    source_img = event['queryStringParameters'].get('source_img')
    
    if source_img:
        media_type = source_img.split('/')[-1].split('.')[-1].lower()
        base64_image = process_image(source_img)
        body = model_body(input_query, base64_image, media_type)
    else:
        body = model_body(input_query)
    
    response = ask_bedrock(bedrock_model_id, body)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

    
