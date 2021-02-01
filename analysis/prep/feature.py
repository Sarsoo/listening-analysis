import datetime
import logging
from csv import DictWriter

from google.cloud import bigquery

from analysis.cache import Cache

from fmframework.net import Network as FMNetwork
from spotframework.net.network import Network as SpotNetwork
from spotframework.model.uri import Uri

logger = logging.getLogger('listening')

def prepare_features(spotnet: SpotNetwork,
                             fmnet: FMNetwork, 
                             cache: Cache,
                             limit: int = None):
    features = populated_features(spotnet=spotnet,
                                  fmnet=fmnet,
                                  cache=cache,
                                  limit=limit)
    save_features(features)

def populated_features(spotnet: SpotNetwork,
                       fmnet: FMNetwork, 
                       cache: Cache,
                       limit: int = None):

    client = bigquery.Client()

    QUERY = (
        'SELECT ' 
        '   DISTINCT uri, track, album, artist '
        'FROM `sarsooxyz.scrobbles.*` '
        'WHERE '
        '  uri IS NOT NULL '
        'ORDER BY artist '
    )

    if limit is not None:
        QUERY += f'LIMIT {limit} '

    logger.info('querying uris')
    query_job = client.query(QUERY)
    rows = query_job.result()

    features = []
    for_pulling = []

    # HIT CACHE
    logger.info('polling cache')
    for row in rows:
        cache_entry = cache.get_track(row.track, row.artist)

        try:
            feature = cache_entry['features']
            features.append(feature)
        except (KeyError, TypeError):
            for_pulling.append(row)
    
    # GET SPOTIFY TRACKS
    logger.info('pulling tracks')
    tracks = spotnet.tracks(uris=[i.uri for i in for_pulling])

    if tracks is not None:
        logger.info('populating features')
        tracks = spotnet.populate_track_audio_features(tracks)
        features += [i.audio_features.to_dict() for i in tracks if i.audio_features is not None]

    logger.info('caching pulled')
    for cacheable in for_pulling:
        track = next((i for i in tracks if str(i.uri) == cacheable.uri), None)
        if track is not None and track.audio_features is not None:
            cache.set_track(name=cacheable.track, artist=cacheable.artist, audio_features=track.audio_features.to_dict())

    return features

def save_features(features):
    date = str(datetime.datetime.now()).replace(':', '.')
    with open(f'{date}_features.csv', 'w', newline='', encoding='UTF-8') as fileobj:
        headers = ['acousticness',
                'analysis_url',
                'danceability',
                'duration_ms',
                'energy',
                'uri',
                'instrumentalness',
                'key',
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