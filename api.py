from asyncio.log import logger
import hashlib
import random
import requests
import sys
import xml.etree.ElementTree as ET

alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
subsonic_version = "1.16.1"
unique_appname = "spotify-to-subsonic-playlists"

class API:
    
    def __init__(self, username, password, server_url):
        self.username=username
        self.salt=''.join(random.choice(alphabet) for i in range(16))
        self.token=hashlib.md5((password+self.salt).encode('utf-8')).hexdigest()
        self.url="{}/rest/".format(server_url)
        self.test_api()

    def test_api(self):
        resp = self.call_endpoint("ping")
        if resp.attrib['status'] != "ok":
            logger.error("failed to make ping request to subsonic server. Stopping execution.")
            sys.exit(1)

    def TEST_call_endpoint(self, endpoint, parameters=None):
        url = self.add_creds(self.url+endpoint)
        # make request
        proxies = {
            "http":None,
            "https":None,
        }
        if parameters is not None:
            for param in parameters:
                url += "&"+ param + "=" + parameters[param]
        print(url)

    def call_endpoint(self, endpoint, parameters=None):       
        url = self.add_creds(self.url+endpoint)
        # make request
        proxies = {
            "http":None,
            "https":None,
        }
        if parameters is not None:
            for param in parameters:
                url += "&"+ param + "=" + parameters[param]
        resp = requests.get(url=url, proxies=proxies)
        parsed_xml = ET.fromstring(resp.text)
        if parsed_xml.attrib['status'] != "ok":
            logger.error("failed to make {} request to subsonic server.".format(endpoint))
        return parsed_xml

    def add_creds(self, url):
        return "{url}.view?u={username}&t={token}&s={salt}&v={ver}&c={appname}".format(url=url, username=self.username, token=self.token, salt=self.salt, ver=subsonic_version, appname=unique_appname)

    