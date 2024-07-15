import logging
import os

class Logger:
    def __init__(self, logpath,name):
        self.logpath = logpath
        self.log_file = name
        self.logger = self.logger_init()

    def logger_init(self):
        """Initialize and configure the logger."""
        logger = logging.getLogger(self.log_file)

        # Avoid adding multiple handlers if logger already exists
        if logger.hasHandlers():
            return logger

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger.setLevel(logging.DEBUG)

        # Ensure log directory exists
        os.makedirs(self.logpath, exist_ok=True)
        filehandler = logging.FileHandler(f"{self.logpath}/{self.log_file}.log")
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

        # Optional: Add console handler
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(logging.DEBUG)
        consolehandler.setFormatter(formatter)
        logger.addHandler(consolehandler)

        logger.info("Logger Initiated")
        return logger

