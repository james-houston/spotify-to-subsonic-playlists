from asyncio.log import logger


def find_song_id(api, name, artist):
    resp = api.call_endpoint("search3", {"query": name})
    if resp[0].find("{http://subsonic.org/restapi}song") is None:
        return None
    # currently returns the first song found that matches the query
    return resp[0].find("{http://subsonic.org/restapi}song").attrib["id"]