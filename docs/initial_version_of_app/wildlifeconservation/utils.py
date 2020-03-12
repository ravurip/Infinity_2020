import time
import logging

from threading import Thread

log = logging.getLogger("digitalhub")

class RunMultipleRequests:

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
