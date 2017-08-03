import json
import csv
import urllib.parse
import boto3
import csv

def handle(event, context):
    print('Loading function')
    s3 = boto3.resource('s3')
    key = event['object'] + '_' + event['id'] +'.csv'    
    filename = '/tmp/'+ event['object'] + '_' + event['id'] +'.csv'
    content = [    
        event['id'],
        event['object'],   
        event['last4'],
        event['type'],
        event['brand'],
        event['exp_month'],
        event['exp_year'],
        event['fingerprint'],
        event['customer'],
        event['country'],
        event['name'],
        event['address_line1'],
        event['address_line2'],
        event['address_city'],
        event['address_state'],
        event['address_zip'],
        event['address_country'],
        event['cvc_check'],
        event['address_line1_check'],
        event['address_zip_check']
    ]
        
    with open(filename, 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(content)
    try:
        bucket = s3.Bucket('etl-8fit')
        response = s3.Object('etl-8fit', key).put(Body=open(filename, 'rb'))        
        
    except Exception as e:        
        raise e

    response = {
        "statusCode": 200,
        "body": 'Created ' + event['object'] + '_' + event['id'] +'.csv' + ' in S3 etl-8fit'
    }    

    return response
