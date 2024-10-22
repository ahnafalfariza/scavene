import logging


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


def setup_logging(log_level, disable_logging=False):
    if disable_logging:
        logging.getLogger().addHandler(NullHandler())
        logging.getLogger().setLevel(logging.CRITICAL + 1)
    else:
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
