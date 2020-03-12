import json
import base64

def lambda_handler(event, context):

    data = json.loads(event)

    # TODO implement
    return {
        'statusCode': 400,
        'body': json.dumps('Hello from Lambda!'),
        'resp': str(base64.b64encode(b"hello")),
        'audio_retieved': data
    }
