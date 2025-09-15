import logging
from logging.handlers import RotatingFileHandler
import yaml
import os

def setup_logger(config):
    log_file = config.get('file', 'logs/ids_lite.log')
    level = getattr(logging, config.get('level','INFO').upper(), logging.INFO)
    max_bytes = config.get('max_bytes', 10*1024*1024)
    backup = config.get('backup_count', 5)

    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger('ids_lite')
    logger.setLevel(level)
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    # console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
