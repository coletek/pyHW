import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

#fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
fmt = '%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger.addHandler(handler)
