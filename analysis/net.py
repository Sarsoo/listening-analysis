import os
from typing import List

import pandas as pd

from spotframework.model.track import PlaylistTrack
from spotframework.net.network import Network as SpotNet, NetworkUser

def get_spotnet():
    return SpotNet(NetworkUser(client_id=os.environ['SPOT_CLIENT'],
                               client_secret=os.environ['SPOT_SECRET'],
                               refresh_token=os.environ['SPOT_REFRESH'])).refresh_access_token()

def get_playlist(name: str, spotnet: SpotNet):
    playlists = spotnet.playlists()
    playlist = [i for i in playlists if i.name == name][0]
    playlist.tracks = spotnet.playlist_tracks(uri=playlist.uri)
    return playlist

def track_frame(tracks: List[PlaylistTrack]):
    return pd.DataFrame(
            [
                [i.track.name, i.track.artists[0].name]
                for i in tracks
            ],
            columns = ["track", "artist"]
        )