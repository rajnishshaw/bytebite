# import modules

import boto3
import json
import base64
import os
import csv
import io


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

def process_csv(source_csv):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=s3_bucket, Key=source_csv)
    csv_content = response['Body'].read().decode('utf-8')
    
    # Process CSV content
    csv_data = []
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    for row in csv_reader:
        csv_data.append(row)
    
    print("csv_data")
    return csv_data

    

# Claude-3 model body
def model_body(input_query, base64_image=None, media_type=None):
    content = [
        {
            "type": "text",
            "text": input_query
        }
    ]
    
    if base64_image and media_type in ['jpg', 'jpeg', 'png', 'gif']:
        content.insert(0, {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": f"image/{media_type}",
                "data": base64_image
            }
        })
    elif base64_image and media_type in ['csv']:
        print("Attaching csv content")
        '''content.insert(0, {
            "type": "document",
            "attrs": {
                "format": "csv",
                "source":{"bytes":base64_image}
            }
            
        })'''

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
        if media_type in ['jpg', 'jpeg', 'png', 'gif']:
            print("PICTURE")
            print(source_img)
            base64_image = process_image(source_img)
            print("PICTURE processed")
        elif media_type in ['csv']:
            print("csv")
            print(source_img)
            print("--------")
            base64_image = process_csv(source_img)
            print("CSV processed")
            
            
        #print(input_query)
        #print(media_type)
        #print(base64_image)
        body = model_body(input_query, base64_image, media_type)
        #body = model_body(input_query)
    else:
        body = model_body(input_query)
    
    response = ask_bedrock(bedrock_model_id, body)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

    
