import datetime
import logging
import string
from csv import DictWriter

from analysis.cache import Cache

from fmframework.net import Network as FMNetwork
from spotframework.net.network import Network as SpotNetwork
from spotframework.model.uri import Uri

logger = logging.getLogger(__name__)

def prepare_scrobbles(spotnet: SpotNetwork,
                      fmnet: FMNetwork, 
                      cache: Cache,
                      from_date: datetime.datetime = None,
                      to_date: datetime.datetime = None,
                      limit: int = None):
    scrobbles = populated_scrobbles(spotnet=spotnet,
                                    fmnet=fmnet,
                                    cache=cache,
                                    from_date=from_date,
                                    to_date=to_date,
                                    limit=limit)
    save_scrobbles(scrobbles)

def populated_scrobbles(spotnet: SpotNetwork,
                        fmnet: FMNetwork, 
                        cache: Cache,
                        from_date: datetime.datetime = None,
                        to_date: datetime.datetime = None,
                        limit: int = None):
    # get all scrobbles for date range
    scrobbles = fmnet.recent_tracks(limit=limit, from_time=from_date, to_time=to_date, page_limit=200)

    punc_stripper = str.maketrans('', '', string.punctuation)

    # populate with uris
    for scrobble in scrobbles:

        cache_entry = cache.get_track(name=scrobble.track.name.lower(), artist=scrobble.track.artist.name.lower())

        try:
            # uri is cached
            scrobble.uri = cache_entry['uri']
        except (TypeError, KeyError): 
            # TypeError for cache_entry == None, KeyError for uri key existing
            # cache missed or doesn't have uri
            logger.info(f'pulling {scrobble.track}')
            spotify_search = spotnet.search(query_types=[Uri.ObjectType.track],
                                            track=scrobble.track.name.translate(punc_stripper),
                                            artist=scrobble.track.artist.name.translate(punc_stripper),
                                            response_limit=5).tracks
            if len(spotify_search) > 0:
                top_result = spotify_search[0]

                if top_result.name.lower() != scrobble.track.name.lower() or top_result.artists[0].name.lower() != scrobble.track.artist.name.lower():
                    logger.info(f'{scrobble.track.name} - {scrobble.track.artist.name} != {top_result.name} - {top_result.artists[0].name}')

                cache.set_track(name=scrobble.track.name.lower(),
                                artist=scrobble.track.artist.name.lower(),
                                uri=str(top_result.uri))
                scrobble.uri = str(top_result.uri)
            else:
                logger.debug('no search tracks returned')
                scrobble.uri = None

    return scrobbles

def save_scrobbles(scrobbles):
    date = str(datetime.datetime.now()).replace(':', '.')
    with open(f'{date}_scrobbles.csv', 'w', newline='', encoding='UTF-8') as fileobj:

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