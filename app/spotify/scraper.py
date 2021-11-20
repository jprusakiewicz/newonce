import base64
import json
from typing import List

import requests

CREDENTIALS_PATH = "./spotify/spotify_credentials.txt"


class Scraper:
    def __init__(self, credentials_path=CREDENTIALS_PATH):
        self.credentials_path = credentials_path
        self.id, self.secret = self.get_auth_credentials()
        self.token = self.get_token()

    def get_auth_credentials(self):
        with open(self.credentials_path, 'rt') as f:
            credentials = json.loads(f.read())

        id = credentials['clientId']
        secret = credentials['clientSecret']
        return id, secret

    def get_auth(self):
        url = "https://accounts.spotify.com/api/token"
        client_creds = f"{self.id}:{self.secret}"
        client_creds_encoded = base64.b64encode(client_creds.encode())
        result = requests.post(url, data={'grant_type': "client_credentials"},
                               headers={'Authorization': f'Basic {client_creds_encoded.decode()}',
                                        'Content-Type': 'application/x-www-form-urlencoded'})
        return result.json()

    def get_token(self) -> str:
        auth_json = self.get_auth()
        access_token = auth_json['access_token']
        return access_token

    def search_spotify_album(self, album_name: str, album_artist: str):
        url = f"https://api.spotify.com/v1/search?type=album&q={album_artist} {album_name}"
        result = requests.get(url, headers={'Authorization': f'Bearer {self.token}',
                                            'Content-Type': 'application/json'})
        albums = result.json()
        album = albums['albums']['items'][0]
        return album

    def get_album_details(self, album_id: str):
        url = f"https://api.spotify.com/v1/albums/{album_id}"
        result = requests.get(url, headers={'Authorization': f'Bearer {self.token}',
                                            'Content-Type': 'application/json'})
        album_details = result.json()
        return album_details

    @staticmethod
    def extract_tracks(album_details: dict) -> List[str]:
        return [track['id'] for track in album_details['tracks']['items']]

    def get_album_tracks(self, album_id):
        album_details = self.get_album_details(album_id)
        album_tracks = self.extract_tracks(album_details)
        return album_tracks

    def get_track(self, track_id: str) -> dict:
        url = f"https://api.spotify.com/v1/track/{track_id}"
        result = requests.get(url, headers={'Authorization': f'Bearer {self.token}',
                                            'Content-Type': 'application/json'})
        return result.json()

    def get_track_features(self, track_id: str) -> dict:
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        result = requests.get(url, headers={'Authorization': f'Bearer {self.token}',
                                            'Content-Type': 'application/json'})
        return result.json()

    def get_tracks_features(self, tracks_ids: List[str]) -> dict:
        url = "https://api.spotify.com/v1/audio-features"
        result = requests.get(url, headers={'Authorization': f'Bearer {self.token}',
                                            'Content-Type': 'application/json'}, params={'ids': ",".join(tracks_ids)})
        return result.json()

    def get_tracks(self, tracks_ids: List[str]) -> dict:
        url = "https://api.spotify.com/v1/tracks"
        result = requests.get(url, headers={'Authorization': f'Bearer {self.token}',
                                            'Content-Type': 'application/json'}, params={'ids': ",".join(tracks_ids)})
        return result.json()

    def get_named_tracks_features(self, tracks_ids: List[str]) -> List[dict]:
        new = []
        features = self.get_tracks_features(tracks_ids)
        basic_details = self.get_tracks(tracks_ids)
        for feature, detail in zip(features['audio_features'], basic_details['tracks']):
            f = feature
            f['name'] = detail['name']
            new.append(f)

        return new

    def get_songs_features(self, album_name: str, artist: str) -> dict:
        album_details = self.search_spotify_album(album_name, artist)
        album_id = album_details['id']
        tracks = self.get_album_tracks(album_id)
        tracks_features = self.get_named_tracks_features(tracks)
        features = {'tracks_features': tracks_features, 'album_details': album_details}
        return features
