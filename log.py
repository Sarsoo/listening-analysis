import logging

logger = logging.getLogger('listening')
spotframework_logger = logging.getLogger('spotframework')
fmframework_logger = logging.getLogger('fmframework')
spotfm_logger = logging.getLogger('spotfm')

logger.setLevel('DEBUG')
spotframework_logger.setLevel('INFO')
fmframework_logger.setLevel('INFO')
spotfm_logger.setLevel('INFO')

log_format = '%(levelname)s %(name)s:%(funcName)s - %(message)s'
formatter = logging.Formatter(log_format)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
spotframework_logger.addHandler(stream_handler)
fmframework_logger.addHandler(stream_handler)
spotfm_logger.addHandler(stream_handler)