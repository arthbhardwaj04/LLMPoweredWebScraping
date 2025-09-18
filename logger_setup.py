import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = "app", level: str = "INFO", logfile: str = "logs/run.log") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, level.upper(), logging.INFO))
    ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    fh = RotatingFileHandler(logfile, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    fh.setLevel(getattr(logging, level.upper(), logging.INFO))
    fh.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s"))

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
