import logging

logger = logging.getLogger('prefix-log')

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

f_handler = logging.FileHandler('f.log')
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

logger.warning('this is warning')
logger.error('this is error')

