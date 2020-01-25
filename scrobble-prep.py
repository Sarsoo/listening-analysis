from fmframework.net.network import Network as FmNet

from spotframework.net.network import Network as SpotNet
from spotframework.net.user import NetworkUser
from spotframework.model.uri import Uri

from csv import DictWriter

import os
import datetime
from log import logger

import analysis.cache

spotnet = SpotNet(NetworkUser(client_id=os.environ['SPOT_CLIENT'],
                              client_secret=os.environ['SPOT_SECRET'],
                              refresh_token=os.environ['SPOT_REFRESH']).refresh_access_token())
fmnet = FmNet(username='sarsoo', api_key=os.environ['FM_CLIENT'])

# initialise cache
cache = analysis.cache.load_cache_from_storage()

# scrobble range
from_date = datetime.datetime(year=2019, month=1, day=1)
to_date = datetime.datetime(year=2020, month=1, day=1)

scrobbles = fmnet.get_recent_tracks(from_time=from_date, to_time=to_date, page_limit=200)

# populate with uris
for scrobble in scrobbles:

    cache_entry = cache.get_track(name=scrobble.track.name.lower(), artist=scrobble.track.artist.name.lower())

    if cache_entry is not None and cache_entry.get('uri'):
        scrobble.uri = cache_entry.get('uri')
    else:
        logger.info(f'pulling {scrobble.track}')
        spotify_search = spotnet.search(query_types=[Uri.ObjectType.track],
                                        track=scrobble.track.name,
                                        artist=scrobble.track.artist.name,
                                        response_limit=5).tracks
        if len(spotify_search) > 0:
            cache.set_track(name=scrobble.track.name.lower(),
                            artist=scrobble.track.artist.name.lower(),
                            uri=str(spotify_search[0].uri))
            scrobble.uri = str(spotify_search[0].uri)
        else:
            logger.debug('no search tracks returned')
            scrobble.uri = None

date = str(datetime.date.today())
with open(f'{date}_scrobbles.csv', 'w', newline='') as fileobj:

    headers = ['track', 'album', 'artist', 'time', 'track id', 'album id', 'artist id', 'uri']
    writer = DictWriter(fileobj, fieldnames=headers, dialect='excel-tab')
    writer.writeheader()

    for scrobble in scrobbles:
        writer.writerow({
            'track': scrobble.track.name,
            'album': scrobble.track.album.name,
            'artist': scrobble.track.artist.name,
            'time': scrobble.time,
            'track id': scrobble.track.mbid,
            'album id': scrobble.track.album.mbid,
            'artist id': scrobble.track.artist.mbid,
            'uri': str(scrobble.uri) if scrobble.uri is not None else ''
        })

analysis.cache.write_cache_to_storage(cache)
