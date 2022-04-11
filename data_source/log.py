import logging

class Q:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.log_handler = logging.StreamHandler()
        self.log_formatter = logging.Formatter(fmt=r'[%(levelname)s] file=%(filename)s time=%(asctime)s :: %(message)s',datefmt=r'%Y-%m-%d %H:%M:%S')
        self.log_handler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.log_handler)

if __name__ == "__main__":
    q = Q()
    q.logger.info('QAQ')
