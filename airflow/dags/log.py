import logging, os
from logging.handlers import RotatingFileHandler


current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)


class CustomHandler(RotatingFileHandler):
    """
    같은 log 메세지 5개 까지만 기록하도록 Custom
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg_dict = {}

    def emit(self, record):
        msg = record.getMessage()
        if msg not in self.msg_dict:
            self.msg_dict[msg] = 0
        if self.msg_dict[msg] < 5:
            super().emit(record)
            self.msg_dict[msg] += 1


logger = logging.getLogger("etl_log")
logger.setLevel(logging.WARNING)
handler = CustomHandler(
    f"{current_directory}/logging/etl_log", maxBytes=2000, backupCount=3
)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
