import unittest
from persistence import TVShow

class TestScraper(unittest.TestCase):

    def test_populate_from_dict(self):
        data = {'episode': u'02',
            'filename': u'CSI.S11E02.Pool.Shark.720p.HDTV.X264-DIMENSION.mkv',
            'name': u'CSI',
            'quality': u'720p',
            'season': u'11',
            'torrent_url': u'http://foo.com/bar.torrent',
            'title': u'Pool Shark (720p .mkv)'}

        show = TVShow(**data)
        for key in data.keys():
            self.assertEqual(show.__dict__[key], data[key])
