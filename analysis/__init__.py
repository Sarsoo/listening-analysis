import logging
import pandas as pd

float_headers = ["acousticness", "danceability", "energy", "instrumentalness", "liveness", "speechiness", "valence"]
descriptor_headers = ["duration_ms", "mode", "loudness", "key", "tempo", "time_signature"] + float_headers

def init_log():
    logger = logging.getLogger('listening')
    spotframework_logger = logging.getLogger('spotframework')
    fmframework_logger = logging.getLogger('fmframework')
    spotfm_logger = logging.getLogger('spotfm')

    logger.setLevel('DEBUG')
    spotframework_logger.setLevel('WARNING')
    fmframework_logger.setLevel('WARNING')
    spotfm_logger.setLevel('WARNING')

    log_format = '%(levelname)s %(name)s:%(funcName)s - %(message)s'
    formatter = logging.Formatter(log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    spotframework_logger.addHandler(stream_handler)
    fmframework_logger.addHandler(stream_handler)
    spotfm_logger.addHandler(stream_handler)
