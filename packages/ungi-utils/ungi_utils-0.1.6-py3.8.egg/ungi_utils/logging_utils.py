#!/usr/bin/env python3

import logging
from ungi_utils.Config import UngiConfig
from pathlib import Path

class UngiLogger:
    def __init__(config):
        self.log_format = config.log_format
        self.log_dir = config.log_dir
        self.log_level = config.log_level
    def get_logger(self):
        logger = logging.getLogger(__name__)
        LogFormat = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler = logging.FileHandler(Path(f"{self.log_dir}/{__name__}.log"))
        file_handler.setFormatter(LogFormat)
        logger.addHandler(file_handler)
        logger.setLevel = self.log_level
        self.logger = logger
        return self.logger
