import logging
import sys

log = logging.basicConfig()


class Log():
    log = None

    def __init__(self, name:str, level: logging._Level = logging.INFO, log_to_file: bool = False, filename: str = None) -> logging.Logger:
        self.log = logging.getLogger(name)
        self.log.setLevel(level)

        handler = logging.FileHandler(filename=filename) if log_to_file else logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s'
        )
        
        handler.setFormatter(formatter)

        self.log.addHandler(handler)

        return self.log
