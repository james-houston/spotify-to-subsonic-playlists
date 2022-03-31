from asyncio.log import logger
from cmath import log
import json
import subsonic_helper

class SpotifyPlaylistManager:
    def __init__(self, spotify_file):
        self.playlists = self.load_spotify_file(spotify_file)

    def load_spotify_file(self, file):
        f = open(file, "r")
        playlists = json.loads(f.read())["playlists"]
        f.close()
        return playlists

    # return list of the names of all tracks in the playlist in the order they appear
    # as well as a map of the format {"title":"artist"}
    # if playlist is empty, return empty list. if the playlist does not exist, returns None.
    def tracks(self, playlist):
        playlist_info = ""
        song_artist_map = {}
        songlist = []
        for pl in self.playlists:
            if pl["name"] == playlist:
                playlist_info = pl
        if playlist_info == "":
            return None
        for track in playlist_info["tracks"]:
            songlist.append(track["track"]["name"])
            song_artist_map[track["track"]["name"]] = track["track"]["artists"][0]["name"]
        return songlist, song_artist_map

class SubsonicPlaylistManager:
    def __init__(self, api):
        self.api = api
        self.playlists = self.get_playlists()
    
    # return playlists map {name:id}
    def get_playlists(self):
        pl = {}
        playlists = self.api.call_endpoint("getPlaylists")
        for p in playlists[0]:
            pl[p.attrib["name"]] = p.attrib["id"]
        return pl    

    def create_playlist(self, playlist_name):
        logger.info("creating playlist {}".format(playlist_name))
        paramters = {"name": playlist_name}
        resp = self.api.call_endpoint("createPlaylist", paramters)
        return resp[0].attrib['id']

    def add_songs_to_playlist(self, songlist_to_add, song_artist_map, playlist_name):
        songs_already_in_playlist, _ = self.get_playlist_songs(playlist_name)
        print(len(songlist_to_add))
        for song in songlist_to_add:
            if song in songs_already_in_playlist:
                continue
            song_id_to_add = subsonic_helper.find_song_id(self.api, song, song_artist_map[song])
            if song_id_to_add is None:
                logger.warn("Unable to find {} by {}".format(song, song_artist_map[song]))
                continue
            self.api.call_endpoint("updatePlaylist", {"playlistId": self.playlists[playlist_name], "songIdToAdd":song_id_to_add})

    def get_playlist_songs(self, playlist_name):
        id = ""
        songs = []
        song_ids = {}
        if playlist_name not in self.playlists:
            id = self.create_playlist(playlist_name)
        else:
            id = self.playlists[playlist_name]
        resp = self.api.call_endpoint("getPlaylist", {"id": id})
        num_tracks = resp[0].attrib['songCount']
        if num_tracks == 0:
            return [], {}
        for song in resp[0]:
            songs.append(song.attrib['title'])
            song_ids[song.attrib['title']] = song.attrib['id']
        return songs, song_ids
        