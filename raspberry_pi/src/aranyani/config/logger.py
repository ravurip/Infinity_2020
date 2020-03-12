import logging

from aranyani.config.config import log_level, log_filename


logging.basicConfig(filename=log_filename)

log = logging.getLogger("aranyani")
log.setLevel(log_level)
