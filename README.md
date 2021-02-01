# Listening Analysis

Notebooks, [analysis](analysis.ipynb) and other [stats](stats.ipynb).

Combining Spotify & Last.fm data for exploring habits and trends
Uses two data sources,

1. Last.fm scrobbles
2. Spotify audio features

The two are joined by searching Last.fm tracks on Spotify to get a Uri, the track name and artist name are provided for the query.
These Uris can be used to retrieve Spotify feature descriptors. `all_joined()` gets a BigQuery of that joins the scrobble time series with their audio features and provides this as a panda frame.