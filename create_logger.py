import logging

def create_logger(name):
    logging.basicConfig(
        level=logging.INFO,
    )
    logger = logging.getLogger(name)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    file_handler = logging.FileHandler(filename="logs/app.log")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger