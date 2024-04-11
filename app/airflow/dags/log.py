import logging, os
from logging.handlers import RotatingFileHandler


current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)

logger = logging.getLogger("etl_log")
logger.setLevel(logging.WARNING)
handler = RotatingFileHandler(
    f"{current_directory}/logging/etl_log", maxBytes=200000, backupCount=1
)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
