from fmframework.net.network import Network as FmNet

from spotframework.net.network import Network as SpotNet
from spotframework.net.user import NetworkUser
from spotframework.model.uri import Uri
from google.cloud import bigquery

from csv import DictWriter

import datetime
import os
from log import logger

import analysis.cache

spotnet = SpotNet(NetworkUser(client_id=os.environ['SPOT_CLIENT'],
                              client_secret=os.environ['SPOT_SECRET'],
                              refresh_token=os.environ['SPOT_REFRESH']).refresh_access_token())
fmnet = FmNet(username='sarsoo', api_key=os.environ['FM_CLIENT'])

cache = analysis.cache.load_cache_from_storage()

client = bigquery.Client()

# Perform a query.
QUERY = (
    'SELECT ' 
    '   DISTINCT uri, track, album, artist '
    'FROM `sarsooxyz.scrobbles.*` '
    'WHERE '
    '  uri IS NOT NULL '
    'ORDER BY artist '
)
logger.info('querying uris')
query_job = client.query(QUERY)
rows = query_job.result()

features = []
for_pulling = []

logger.info('polling cache')
for row in rows:
    cache_entry = cache.get_track(row.track, row.artist)

    if cache_entry is not None:
        if cache_entry.get('features') is None:
            features.append(cache_entry)
            continue

    for_pulling.append(row)

logger.info('pulling tracks')
tracks = spotnet.get_tracks(uri_strings=[i.uri for i in for_pulling])

if tracks is not None:
    logger.info('populating features')
    tracks = spotnet.populate_track_audio_features(tracks)
    features += [i.audio_features.to_dict() for i in tracks if i.audio_features is not None]

logger.info('caching pulled')
for cacheable in for_pulling:
    track = next((i for i in tracks if str(i.uri) == cacheable.uri), None)
    if track is not None and track.audio_features is not None:
        cache.set_track(name=cacheable.track, artist=cacheable.artist, audio_features=track.audio_features.to_dict())

logger.info('dumping')
date = str(datetime.date.today())
with open(f'{date}_features.csv', 'w', newline='') as fileobj:

    headers = ['acousticness',
               'analysis_url',
               'danceability',
               'duration_ms',
               'energy',
               'uri',
               'instrumentalness',
               'key',
               'key_code',
               'liveness',
               'loudness',
               'mode',
               'speechiness',
               'tempo',
               'time_signature',
               'track_href',
               'valence']
    writer = DictWriter(fileobj, fieldnames=headers, dialect='excel-tab')
    writer.writeheader()

    for feature in features:
        writer.writerow(feature)

analysis.cache.write_cache_to_storage(cache)
