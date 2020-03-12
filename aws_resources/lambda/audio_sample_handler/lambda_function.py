import json
from base64 import b64decode
import boto3

def lambda_handler(event, context):
    data = json.loads(event)

    audio_data = data['audio_particulars']
    metadata = data['metadata']
    filename=audio_data['filename']

    audio_encoded = audio_data['audio_encoded']

    if audio_encoded:
        audio_string_content = bytes(audio_data['audio_data']).decode("utf-8")
        s3_filekey = f'infinity/aranyani/{filename}'

        s3 = boto3.resource('s3')
        object = s3.Object('gupthas-garage', s3_filekey)

        audio_binary_data = b64decode(audio_string_content)

        object.put(Body=audio_binary_data)

    # TODO implement
    return {
        'statusCode': 400,
        'body': json.dumps('Hello from Lambda!'),
        'stored': audio_encoded,
        'audio_key': data
    }
