from aranyani import AUDIO_SAMPLE_RECORD, AudioSampleHandler, Communicator, log

CONF = AUDIO_SAMPLE_RECORD
try:
    audio_handler = AudioSampleHandler(RATE=CONF['RATE'], CHUNK=CONF['CHUNK'], TO_CACHE=CONF['TO_CACHE'])
    communicator = Communicator()
    while True:
        try:
            interrupt = int(input("Enter any int value"))
            message = audio_handler.snip_audio_sample(interrupt)
            resp = communicator.push_audio_file(message)
            log.info(f"Successfully posted alert for the audio snip {str(resp.text)}, {resp.status_code}")

        except NameError as e:
            log.warning("Invalid value entered")
            continue

except Exception as e:
    log.error("Application terminated with exception", e)
    exit(1)
