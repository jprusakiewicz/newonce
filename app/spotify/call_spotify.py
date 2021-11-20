import base64
import json
from typing import List

import requests


def get_auth_credentials():
    cred_path = "./spotify/spotify_credentials.txt"
    with open(cred_path, 'rt') as f:
        credentials = json.loads(f.read())

    id = credentials['clientId']
    secret = credentials['clientSecret']
    return id, secret


def get_auth():
    id, secret = get_auth_credentials()
    url = "https://accounts.spotify.com/api/token"
    client_creds = f"{id}:{secret}"
    client_creds_encoded = base64.b64encode(client_creds.encode())
    result = requests.post(url, data={'grant_type': "client_credentials"},
                           headers={'Authorization': f'Basic {client_creds_encoded.decode()}',
                                    'Content-Type': 'application/x-www-form-urlencoded'})
    return result.json()


def get_token() -> str:
    auth_json = get_auth()
    access_token = auth_json['access_token']
    return access_token


def search_spotify_album(album_name: str, album_artist: str):
    url = f"https://api.spotify.com/v1/search?type=album&q={album_artist} {album_name}"
    token = get_token()
    result = requests.get(url, headers={'Authorization': f'Bearer {token}',
                                        'Content-Type': 'application/json'})
    albums = result.json()
    album = albums['albums']['items'][0]
    return album


def get_album_details(album_id: str):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    token = get_token()
    result = requests.get(url, headers={'Authorization': f'Bearer {token}',
                                        'Content-Type': 'application/json'})
    album_details = result.json()
    return album_details


def extract_tracks(album_details: dict) -> List[str]:
    return [track['id'] for track in album_details['tracks']['items']]


def get_album_tracks(album_id):
    album_details = get_album_details(album_id)
    album_tracks = extract_tracks(album_details)
    return album_tracks


def get_track(track_id: str) -> dict:
    url = f"https://api.spotify.com/v1/track/{track_id}"
    token = get_token()
    result = requests.get(url, headers={'Authorization': f'Bearer {token}',
                                        'Content-Type': 'application/json'})
    return result.json()


def get_track_features(track_id: str) -> dict:
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    token = get_token()
    result = requests.get(url, headers={'Authorization': f'Bearer {token}',
                                        'Content-Type': 'application/json'})
    return result.json()


def get_tracks_features(tracks_ids: List[str]) -> dict:
    url = "https://api.spotify.com/v1/audio-features"
    token = get_token()
    result = requests.get(url, headers={'Authorization': f'Bearer {token}',
                                        'Content-Type': 'application/json'}, params={'ids': ",".join(tracks_ids)})
    return result.json()


def get_tracks(tracks_ids: List[str]) -> dict:
    url = "https://api.spotify.com/v1/tracks"
    token = get_token()
    result = requests.get(url, headers={'Authorization': f'Bearer {token}',
                                        'Content-Type': 'application/json'}, params={'ids': ",".join(tracks_ids)})
    return result.json()


def get_named_tracks_features(tracks_ids: List[str]) -> List[dict]:
    new = []
    features = get_tracks_features(tracks_ids)
    basic_details = get_tracks(tracks_ids)
    for feature, detail in zip(features['audio_features'], basic_details['tracks']):
        f = feature
        f['name'] = detail['name']
        new.append(f)

    return new


def get_songs_features(album_name: str, artist: str) -> dict:
    album_details = search_spotify_album(album_name, artist)
    album_id = album_details['id']
    tracks = get_album_tracks(album_id)
    tracks_features = get_named_tracks_features(tracks)
    features = {'tracks_features': tracks_features}
    features['album_details'] = album_details
    return features
