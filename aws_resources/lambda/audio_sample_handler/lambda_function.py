import json
from aranyani_listner import post_audio_to_s3


def lambda_handler(event, context):

    method_to_invoke = {
        "audio": post_audio_to_s3
    }

    try:
        data = json.loads(event)

        event_type = data['eventType']
        event_data = data['data']
        metadata = data['metadata']

        operation_response = method_to_invoke[event_type](event_data, metadata)

        return {'statusCode': 200, 'lambda_response': operation_response}

    except Exception as exc:
        return {'statusCode': 501, 'error': "Failed to resolve the eventType provided", 'errorDescription': str(exc)}
