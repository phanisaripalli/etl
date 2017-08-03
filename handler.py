import json

def executor(event, context):
    body = {
        "message": "Successfully copied to RDS and added to the Bucket",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response