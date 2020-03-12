from aranyani import AUDIO_SAMPLE_RECORD, AudioSampleHandler, log

CONF = AUDIO_SAMPLE_RECORD
try:
    audio_handler = AudioSampleHandler(RATE=CONF['RATE'], CHUNK=CONF['CHUNK'], TO_CACHE=CONF['TO_CACHE'])
    while True:
        try:
            interrupt = int(input("Enter any int value"))
            audio_handler.snip_audio_sample(interrupt)
        except NameError as e:
            log.warning("Invalid value entered")
            continue

except Exception as e:
    log.error("Application terminated with exception", e)
    exit(1)
