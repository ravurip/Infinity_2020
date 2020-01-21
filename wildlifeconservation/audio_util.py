import pyaudio
import wave
import time
import logging

from queue import Queue

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
        self.length = int((RATE/CHUNK)*60)
        self.audio_queue = self.__init_audio_frames_que()

    def __init_audio_frames_que(self):
        return Queue()

    def __trim_queue(self):
        while self.audio_queue.qsize() > self.length:
            self.audio_queue.get()

    def append_audio_stream_to_queue(self):
        self.audio_port = pyaudio.PyAudio()
        self.audio_stream = self.audio_port.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, frames_per_buffer=self.CHUNK, input=True)

        try:
            while True:
                data = self.audio_stream.read(self.CHUNK)
                self.audio_queue.put(data)
                self.__trim_queue()

        except Exception as e:
            print("Exception reading the audio from audio port. ", e)
            raise e

        finally:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_port.terminate()

    def write_audio_wave_file(self, name):
        wf = wave.open(name, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio_port.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(list(self.audio_queue.queue)))
        wf.close()


if __name__ == "__mainw__":
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
