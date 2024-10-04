# GenAI-CaterAssistant (Bytebite )

Install the following python modules


## Description


## Getting Started
### Pre-requisites
* AWS Account setup
* Access to Amazon Bedrock Foundational model
* Sagemaker Studio / Local IDE
 
#### Environment setup
#### 1. Clone GitRepo to local machine

Create a folder names "ByteBite"

```
mkdir ByteBite && cd ByteBite

```
Clone the GitRepo to your local machine.
```
git clone https://github.com/rajnishshaw/bytebite.git
cd bytebite-main
```
#### 2. AWS stack deployment
* Login to your AWS account
* Follow the steps in the reference to grant access to the Amazon Bedrock foundational model
  - https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html
    - Note: This demo uses Claude3 model.Ensure access is granted to Claude3 model.
* Go to AWS cloudformation service and create a new stack using "cf_template.yaml" file

#### 3. Test API Gateway
* On the CloudFormation Resources tab, locate the logical ID "Api" and click the corresponding Physical ID to open the URL.
* Append **"/byteBite"** to the URL. if the output is **"Hello from byteBite Lambda!"**, proceed to next.


#### 4. Upload Lambda code
* Go to Lamba service
* Search for **"byteBite"** . upload the **"/Code/Lambda/byteBiteLambda.zip"** file to the lambda function and deploy the function.


#### 5. Setup UI
UI is based on streamlit. If your local laptop has AWS environment setup along with python, follow the steps below.
* Install the following python modules
```
pip install boto3
pip install requests
pip install streamlit
pip install streamlit_option_menu
```
* Go to /code/gui/byteBite/utils/common.py
* Replace "<<S3_BUCKET_NAME>>" with S3 bucket name created by the cloudformation
* Replace "<< API-URL>>" with API gateway end point created by the cloudformation
* Save the changes
* Go to terminal , ensure your aws credentials are set in environment variable 
* Start the UI
```
  cd /code/gui/byteBite
  streamlit run app.py
```
##### Optional: Buidling front end on sagemaker studio
* Login into your sagemaker studio. Go to Terminal
* Ensure role has access to the S3 bucket that created part of the stack.
* Install the following python modules
```
pip install boto3
pip install requests
pip install streamlit
pip install streamlit_option_menu
```
* Upload the contents of frontEnd directory
* Open file front_end_v7.py
* Replace "<<S3_BUCKET_NAME>>" with S3 bucket name created by the cloudformation
* Replace "<< API-URL>>" with API gateway end point created by the cloudformation
* Save the changes
* Start the UI
```
cd /code/gui/byteBite
  streamlit run app.py
```
#### 6. Access UI
If you are using your laptop for streamlit application, use https://localhost:8501.

For the Sagemaker studio setup,

* On the Sagemaker studio url copy until default/ and append proxy/8501/
  - Example:
    - ** "https://<xxxxx>.studio.us-east-1.sagemaker.aws/jupyter/default/" replace
      with
      ** "https://<xxxxx>.studio.us-east-1.sagemaker.aws/jupyter/default/proxy/8501/"


#### 7. Cleanup
* Go to Sagemaker studio terminal window. < Ctrl>+C to kill the app.py
* Go to AWS console, cloudformation, and delete the stack.

