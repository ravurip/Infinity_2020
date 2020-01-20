import pyaudio
import wave
import time
import logging

from queue import Queue
from collections import deque

from threading import Thread

log = logging.getLogger("digitalhub")


class SampleDispatcher:

    def __init__(self, target, num_of_threads, **kwargs):
        self.target = target
        self.kwargs = kwargs
        self.threads = self.run_threads(num_of_threads)
        log.info(f"Created {num_of_threads} threads to post requests.")

    def ensure_all_threads_closed(self):
        log.info("In Progress")
        while len([t for t in self.threads if t.is_alive()]) > 0:
            time.sleep(1)
        log.info("All threads terminated.")

    def run_threads(self, num_of_threads):
        threads = []

        for i in range(num_of_threads):
            thread = Thread(target=self.target, kwargs=self.kwargs)
            threads.append(thread)
            thread.start()
            log.debug(f"Started thread {i}")
            time.sleep(1.5 / num_of_threads)

        return threads


class AudioSampleStreamer:

    def __init__(self, CHUNK = 1024, FORMAT = pyaudio.paInt16, CHANNELS = 1, RATE = 44100):
        self.RATE = RATE
        self.CHUNK = CHUNK
        self.FORMAT = FORMAT
        self.CHANNELS = CHANNELS
        self.audio_queue = self.__init_audio_frames_que()

    def __init_audio_frames_que(self):
        return Queue()

    def __trim_queue(self, length):
        while self.audio_queue.qsize() > length:
            self.audio_queue.get()

    def __init_audio_stream_to_queue(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

        return stream


if __name__ == "__main__":
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 30
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        print(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
