# Listening Analysis

Notebooks, [analysis](analysis.ipynb), [artists](artist.ipynb) & [playlist](playlist.ipynb) investigations and other [stats](stats.ipynb).

Combining Spotify & Last.fm data for exploring habits and trends
Uses two data sources,

1. Last.fm scrobbles
2. Spotify audio features

The two are joined by searching Last.fm tracks on Spotify to get a Uri, the track name and artist name are provided for the query.
These Uris can be used to retrieve Spotify feature descriptors.