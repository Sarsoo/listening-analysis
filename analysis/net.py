import os
from typing import List

import pandas as pd

from spotframework.model.track import PlaylistTrack
from spotframework.net.network import Network as SpotNet, NetworkUser
from fmframework.net.network import Network as FMNet

def get_spotnet():
    return SpotNet(NetworkUser(client_id=os.environ['SPOT_CLIENT'],
                               client_secret=os.environ['SPOT_SECRET'],
                               refresh_token=os.environ['SPOT_REFRESH'])).refresh_access_token()

def get_fmnet():
    return FMNet(username='sarsoo', api_key=os.environ['FM_CLIENT'])

playlist_cache = dict() # low-tech caches for repeated pulling 
all_playlists = list()
def get_playlist(name: str, spotnet: SpotNet):
    global all_playlists
    try:
        return playlist_cache[name]
    except KeyError:
        if len(all_playlists) == 0:
            all_playlists = spotnet.playlists()
        playlist = [i for i in all_playlists if i.name == name][0]
        playlist.tracks = spotnet.playlist_tracks(uri=playlist.uri)
        playlist_cache[name] = playlist
        return playlist

def track_frame(tracks: List[PlaylistTrack]):
    return pd.DataFrame(
            [
                [i.track.name, i.track.artists[0].name]
                for i in tracks
            ],
            columns = ["track", "artist"]
        )