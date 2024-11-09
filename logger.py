import logging

def setup_logger():
    logging.basicConfig(
        filename='cinematicket.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )

def log_event(message):
    logging.info(message)
