
import logging
log_format = "%(levelname)s-[%(asctime)s][%(module)s][%(funcName)s][%(lineno)d]: %(message)s"
logging.basicConfig(level=logging.WARNING, format=log_format)
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
