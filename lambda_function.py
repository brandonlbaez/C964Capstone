import os
import io
import boto3
import json
import csv

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    payload = str(event).translate({ord(i): None for i in "[]'"})

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='text/csv',
                                       Body=payload)
                                       
    result = json.loads(response['Body'].read().decode())
    print(result)
    prediction = round((result * 100), 2)
    
    return {
        'isBase64Encoded': True,
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'multiValueHeaders': {},
        'body': json.dumps(prediction)
    }