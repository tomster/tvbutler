import unittest
from scraper import extract_metadata

class TestScraper(unittest.TestCase):

    def test_episode_extraction(self):
        data = extract_metadata(u"""Show Name:The Daily Show with Jon Stewart; 
            Show Title: Justin Timberlake; Season: 2010; Episode: 09.30; 
            Filename: the.daily.show.2010.09.30.hdtv.xvid-fqm.avi;""")
        self.assertEqual(data['name'], u'The Daily Show with Jon Stewart')
        self.assertEqual(data['title'], u'Justin Timberlake')
        self.assertEqual(data['season'], u'2010')
        self.assertEqual(data['episode'], u'09.30')
        self.assertEqual(data['filename'], u'the.daily.show.2010.09.30.hdtv.xvid-fqm.avi')

    def test_episode_extraction_720p(self):
        data = extract_metadata(u"""Show Name:CSI; Show Title:  Pool Shark (720p .mkv); Season: 11; 
    Episode: 02; Filename: CSI.S11E02.Pool.Shark.720p.HDTV.X264-DIMENSION.mkv;""")
        self.assertEqual(data['name'], u'CSI')
        self.assertEqual(data['title'], u'Pool Shark (720p .mkv)')
        self.assertEqual(data['season'], u'11')
        self.assertEqual(data['episode'], u'02')
        self.assertEqual(data['filename'], u'CSI.S11E02.Pool.Shark.720p.HDTV.X264-DIMENSION.mkv')
