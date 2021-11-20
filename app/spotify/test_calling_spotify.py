import unittest

from .call_spotify import search_spotify_album, get_token, get_album_tracks, \
    get_named_tracks_features


class MyTestCase(unittest.TestCase):
    def test_calling_spotify(self):
        # given
        given_album_name = "alles wird gut"
        given_artist = "kummer"
        expected_id = "2uZ1heDjBsSvxnANhH8EmD"
        # when
        album = search_spotify_album(given_album_name, given_artist)
        album_id = album['id']
        # then
        self.assertEqual(album_id, expected_id)

    def test_getting_token(self):
        # when
        token = get_token()
        # then
        self.assertIsInstance(token, str)

    def test_getting_album_tracks(self):
        # given
        album_id = "2up3OPMp9Tb4dAKM2erWXQ"
        expected_tracks = ['7nmA2R4IQSfZpMYFhXY9r7', '4AHIgOApMmqVfpvc1hxK6x']
        # when
        tracks = get_album_tracks(album_id)
        # then
        self.assertListEqual(expected_tracks, tracks)

    def test_getting_tracks_features(self):
        # given
        tracks = ['7nmA2R4IQSfZpMYFhXY9r7', '4AHIgOApMmqVfpvc1hxK6x']
        # when
        tracks_features = get_named_tracks_features(tracks)
        # then
        self.assertIsInstance(tracks_features, list)


if __name__ == '__main__':
    unittest.main()
