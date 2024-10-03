import boto3
import requests

#replace these based on your actual configurations
api_gw_url = '<<API-URL>>'
s3_bucket = '<<S3_BUCKET_NAME>>'
s3_prefix = 'images/'

# ask genAI model with Image/ Text
def ask_model(source_img, input_query):
    url = api_gw_url
    if source_img != None:
        params = {'source_img': s3_prefix + source_img, 'input_query': input_query}
    else:
        params = {'input_query': input_query}
    response = requests.get(url, params)
    return (f"Assistant: {response.json()}")


# s3 upload function
def s3_upload(file):
    prefix_path = s3_prefix + file.name
    s3 = boto3.client('s3')
    try:
        s3.upload_fileobj(
            file,
            s3_bucket,
            prefix_path
            )
        return prefix_path
    except:
        return None

