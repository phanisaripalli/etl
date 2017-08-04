
import json
import urllib.parse
import boto3
import sys 
import datetime

print('Loading function')


def excutor(event, context):
    import uuid
    now = uuid.uuid4().hex
    
    print(now)
   
    client = boto3.client('stepfunctions')
    try:
        response = client.start_execution(stateMachineArn='xxxxxxxxxxxxx',name='ETLStepMachine-' +now, input = json.dumps(event))
    except:        
        print (sys.exc_info()[0])
        return False
         
    return True