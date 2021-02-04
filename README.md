# Listening Analysis

Notebooks:
* [analysis](analysis.ipynb) for a intro to the dataset and premise
* [artist](artist.ipynb), [album](./album.ipynb) & [playlist](playlist.ipynb) investigations
* [stats](stats.ipynb) for high-level stats about the dataset (Spotify feature miss ratio)
* [playlist classifier](./playlist-classifier.ipynb) using Scikit to classify tracks using the contents of playlists as models

Combining Spotify & Last.fm data for exploring habits and trends
Uses two data sources,

1. Last.fm scrobbles
2. Spotify audio features

The two are joined by searching Last.fm tracks on Spotify to get a Uri, the track name and artist name are provided for the query.
These Uris can be used to retrieve Spotify feature descriptors.