from datetime import datetime
import logging
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

float_headers = ["acousticness", "danceability", "energy", "instrumentalness", "liveness", "speechiness", "valence"]
spotify_descriptor_headers = ["duration_ms", "mode", "loudness", "key", "tempo", "time_signature"] + float_headers

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

def days_since(in_date):
    # only using up to end of 2020 in dataset at the moment
    now = datetime(year=2021, month=1, day=1)
    return now - in_date