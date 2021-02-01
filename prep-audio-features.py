import datetime
import os
from dotenv import load_dotenv

from fmframework.net.network import Network as FMNet
from spotframework.net.network import Network as SpotNet, NetworkUser
from spotframework.model.uri import Uri

from analysis.prep.feature import prepare_features
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
    prepare_features(spotnet, fmnet, cache)
except Exception as e:
    print(f"Error Occured: {e}")
finally:
    write_cache_to_storage(cache)