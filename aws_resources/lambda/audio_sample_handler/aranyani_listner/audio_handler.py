import boto3
from base64 import b64decode

from aranyani_listner import S3_BUCKET, AUDIO_FILES_PATH, get_current_date


def post_audio_to_s3(audio_data, metadata):
    filename = audio_data['filename']

    try:
        audio_encoded = audio_data['audio_encoded']
        if audio_encoded:
            audio_string_content = audio_data['audio_data']
            audio_b64 = audio_string_content.encode("utf-8")

            host = metadata['hostname']
            date = get_current_date()

            s3_filekey = f'{AUDIO_FILES_PATH}{host}/{date}/{filename}'

            s3 = boto3.resource('s3')
            object = s3.Object(S3_BUCKET, s3_filekey)

            audio_binary_data = b64decode(audio_b64)

            object.put(Body=audio_binary_data)

            return {"audio_s3_path": f"s3://{S3_BUCKET}/{s3_filekey}"}

    except Exception as exc:
        raise exc
