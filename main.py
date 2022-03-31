from api import API
from playlists import SpotifyPlaylistManager, SubsonicPlaylistManager
import json

config_file = "config.json"

def dev_func(spot_pm, sub_pm, playlist_name):
    # focus on My Top Songs 2016 to start
    songlist, song_artist_map = spot_pm.tracks(playlist_name)
    sub_pm.add_songs_to_playlist(songlist, song_artist_map, playlist_name)



# Read config file
f = open(config_file, "r")
config = json.loads(f.read())
f.close()

# create object for api calls
api = API(config["username"], config["password"], config["subsonic_url"])

# load spotify playlists
spot_pm = SpotifyPlaylistManager(config["playlist_file"])

# load subsonic playlists
sub_pm = SubsonicPlaylistManager(api)

dev_func(spot_pm, sub_pm, "My Top Songs 2016")