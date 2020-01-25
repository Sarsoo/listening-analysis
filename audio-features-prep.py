from fmframework.net.network import Network as FmNet

from spotframework.net.network import Network as SpotNet
from spotframework.net.user import NetworkUser
from spotframework.model.uri import Uri

from csv import DictWriter

import os
import datetime
import json
from log import logger

spotnet = SpotNet(NetworkUser(client_id=os.environ['SPOT_CLIENT'],
                              client_secret=os.environ['SPOT_SECRET'],
                              refresh_token=os.environ['SPOT_REFRESH']).refresh_access_token())
fmnet = FmNet(username='sarsoo', api_key=os.environ['FM_CLIENT'])


