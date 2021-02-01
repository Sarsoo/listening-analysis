import datetime
import os
from dotenv import load_dotenv

from fmframework.net.network import Network as FMNet
from spotframework.net.network import Network as SpotNet, NetworkUser
from spotframework.model.uri import Uri

from analysis.prep.scrobble import prepare_scrobbles, populated_scrobbles
from analysis.cache import load_cache_from_storage, write_cache_to_storage
from analysis import init_log

load_dotenv()
init_log()

spotnet = SpotNet(NetworkUser(client_id=os.environ['SPOT_CLIENT'],
                              client_secret=os.environ['SPOT_SECRET'],
                              refresh_token=os.environ['SPOT_REFRESH'])).refresh_access_token()
fmnet = FMNet(username='sarsoo', api_key=os.environ['FM_CLIENT'])
cache = load_cache_from_storage()

try:
    for year in range(2017, 2021):
        from_date = datetime.datetime(year=year, month=1, day=1)
        to_date = datetime.datetime(year=year + 1, month=1, day=1)

        print(f"Getting {year}")

        prepare_scrobbles(spotnet, fmnet, cache, from_date, to_date)
except Exception as e:
    print(f"Error Occured: {e}")
finally:
    write_cache_to_storage(cache)