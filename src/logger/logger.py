import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

full_log = logging.FileHandler("logs/full.log", "a", "utf-8")
full_log.setLevel(logging.DEBUG)
full_log.setFormatter(formatter)
logger.addHandler(full_log)

error_log = logging.FileHandler("logs/errors.log", "a", "utf-8")
error_log.setLevel(logging.WARNING)
error_log.setFormatter(formatter)
logger.addHandler(error_log)
