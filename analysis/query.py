
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

def all_joined(limit: int = 200):
    query = (
        'SELECT ' 
        '   Scrobbles.track, Scrobbles.album, Scrobbles.artist, Scrobbles.time, Scrobbles.uri, '
        '   Features.acousticness, Features.danceability, Features.duration_ms, '
        '   Features.energy, Features.instrumentalness, Features.key, Features.liveness, '
        '   Features.loudness, Features.mode, Features.speechiness, Features.tempo, ' 
        '   Features.time_signature, Features.valence '

        'FROM `sarsooxyz.scrobbles.*` AS Scrobbles '
        'INNER JOIN `sarsooxyz.audio_features.features` AS Features '
        'ON Scrobbles.uri = Features.uri '
    )

    if limit >= 0:
        query += f' LIMIT {limit}'

    return client.query(query).to_dataframe()

def get_query(pull=False, cache="query.csv"):
    if pull:
        scrobbles = all_joined(limit=-1) # load dataset as panda frame
    else:
        scrobbles = pd.read_csv(cache, sep='\t', index_col=0)
    scrobbles['time'] = pd.to_datetime(scrobbles['time'])
    scrobbles = scrobbles.set_index('time')
    return scrobbles