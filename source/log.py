import os
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler


class LogHandler(RotatingFileHandler):

    def __init__(self, *args, **kwargs):
        LogHandler.log_folder_create()
        self.start_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        super().__init__(*args, **kwargs)

    @staticmethod
    def log_folder_create():
        if not os.path.exists("log"):
            os.mkdir("log")

    def doRollover(self):
        name = f'{self.start_time} till {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log'
        self.rotate(self.baseFilename, f"log/{name}")
        self.start_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        super().doRollover()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        LogHandler(
            f"log/debug.log",
            mode='a',
            maxBytes=250000
        )
    ]
)
