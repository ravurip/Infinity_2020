import pyaudio
import wave
import time
import logging

from queue import Queue

from threading import Thread

log = logging.getLogger("digitalhub")


class AudioSampleStreamer:

    def __init__(self, CHUNK = 1024, FORMAT = pyaudio.paInt16, CHANNELS = 1, RATE = 44100):
        self.RATE = RATE
        self.CHUNK = CHUNK
        self.FORMAT = FORMAT
        self.CHANNELS = CHANNELS
        self.length = int((RATE/CHUNK)*60)
        self.audio_queue = self.__init_audio_frames_que()
        log.info(f"Initialised Audio sample streamer.")

    def __init_audio_frames_que(self):
        return Queue()

    def __trim_queue(self):
        while self.audio_queue.qsize() > self.length:
            self.audio_queue.get()

    def append_audio_stream_to_queue(self):
        self.audio_port = pyaudio.PyAudio()
        self.audio_stream = self.audio_port.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, frames_per_buffer=self.CHUNK, input=True)

        try:
            log.info("Audio samples streaming in.")
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

    def write_audio_wave_file(self, filename, num_of_seconds):

        num_of_frames = int((self.RATE/self.CHUNK)*num_of_seconds)
        frames = list(self.audio_queue.queue)[-num_of_frames:]

        wf = wave.open(filename, 'wb')
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

    def ensure_all_threads_closed(self):
        log.info("In Progress")
        while len([t for t in self.threads if t.is_alive()]) > 0:
            time.sleep(1)
        log.info("All threads terminated.")

    def run_threads(self, target, name, **kwargs):
        thread = Thread(target=target, name=name, kwargs=kwargs)
        self.threads.append(thread)
        thread.start()
        log.debug(f"Started thread {name}")

    def init_audio_stream_collection(self):
        self.run_threads(target=self.append_audio_stream_to_queue, name="audio_stream_reader")

    def snip_audio_sample(self, filename, seconds=60):
        self.run_threads(target=self.write_audio_wave_file, name="audio_stream_stripper", filename=filename, num_of_seconds=seconds)


if __name__ == "__main__":
    pass