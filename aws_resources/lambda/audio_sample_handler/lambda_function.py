import json


def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 400,
        'body': json.dumps('Hello from Lambda!'),
        'msg': event['key1']
    }
