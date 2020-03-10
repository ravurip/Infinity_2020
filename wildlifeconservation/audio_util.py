import pyaudio
import wave
import time
import logging

from queue import Queue

from threading import Thread

log = logging.getLogger("aranyani")


class AudioSampleStreamer:

    def __init__(self, CHUNK=128, FORMAT=pyaudio.paInt16, CHANNELS=1, RATE=48000, TO_CACHE=1500):
        self.RATE = RATE
        self.CHUNK = CHUNK
        self.FORMAT = FORMAT
        self.CHANNELS = CHANNELS
        self.length = int((RATE / CHUNK) * TO_CACHE)
        self.audio_queue = Queue()
        self.audio_port = pyaudio.PyAudio()
        self.audio_stream = self.audio_port.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, frames_per_buffer=self.CHUNK, input=True)
        log.info(f"Initialised Audio sample streamer with a sampling rate of {RATE} and the chunk size is {CHUNK}")

    def trim_queue(self):
        while True:
            print(str(self.audio_queue.qsize() > self.length))
            if self.audio_queue.qsize() > self.length:
                self.audio_queue.get()

    def append_audio_stream_to_queue(self):
        try:
            log.info(f"Audio samples streaming in. Buffer width is {str(self.CHUNK / self.RATE)} seconds")
            while True:
                data = self.audio_stream.read(self.CHUNK, exception_on_overflow=False)
                self.audio_queue.put(data)

        except OSError as e:
            log.warning("Audio stream or Audio port cosed. Stopping Application")
            raise e

        except Exception as e:
            print("Exception reading the audio from audio port. ", e)
            raise e

    def terminate_audio_stream_collection(self):
        try:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_port.terminate()

        except Exception as e:
            log.error("Failed to close audio port or stream. ", e)
            raise e

    def write_audio_wave_file(self, filename, num_of_seconds):

        num_of_frames = int((self.RATE / self.CHUNK) * num_of_seconds)
        frames = list(self.audio_queue.queue)[-num_of_frames:]

        wf = wave.open(filename + ".wav", 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio_port.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def detect_activity(self):
        pass


class AudioSampleHandler(AudioSampleStreamer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.threads = []
        self.init_audio_stream_collection()
        self.init_audio_stream_truncate()

    def ensure_all_threads_closed(self):
        log.info("In Progress")
        while len([t for t in self.threads if t.is_alive()]) > 0:
            time.sleep(1)
        log.info("All threads terminated.")

    def run_threads(self, target, name, daemon, **kwargs):
        thread = Thread(target=target, name=name, kwargs=kwargs, daemon=daemon)
        self.threads.append(thread)
        thread.start()
        log.debug(f"Started thread {name}")

    def init_audio_stream_collection(self):
        self.run_threads(target=self.append_audio_stream_to_queue, name="audio_stream_reader", daemon=True)

    def init_audio_stream_truncate(self):
        self.run_threads(target=self.trim_queue, name="audio_queue_truncate", daemon=True)

    def snip_audio_sample(self, filename, seconds=45):
        self.run_threads(target=self.write_audio_wave_file, name="audio_stream_stripper", daemon=False, filename=filename, num_of_seconds=seconds)


if __name__ == "__main__":
    try:
        audio_handler = AudioSampleHandler()
        while True:
            try:
                interrupt = int(input("Enter any int value"))
                audio_handler.snip_audio_sample(f"hello_{interrupt}", interrupt)
            except NameError as e:
                log.warning("Invalid value entered")
                continue

    except Exception as e:
        log.error("Application terminated with exception", e)
        exit(1)
