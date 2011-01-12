import unittest
from tvbutler.scraper import extract_metadata

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
        self.assertEqual(data['quality'], u'sd')

    def test_episode_extraction_720p(self):
        data = extract_metadata(u"""Show Name:CSI; Show Title:  Pool Shark (720p .mkv); Season: 11; 
    Episode: 02; Filename: CSI.S11E02.Pool.Shark.720p.HDTV.X264-DIMENSION.mkv;""")
        self.assertEqual(data['name'], u'CSI')
        self.assertEqual(data['title'], u'Pool Shark (720p .mkv)')
        self.assertEqual(data['season'], u'11')
        self.assertEqual(data['episode'], u'02')
        self.assertEqual(data['filename'], u'CSI.S11E02.Pool.Shark.720p.HDTV.X264-DIMENSION.mkv')
        self.assertEqual(data['quality'], u'720p')

    def test_episode_extraction_with_colon_in_name(self):
        data = extract_metadata(u"""Show Name:Law & Order: Whatever; Show Title: Shit: it went down; Season: 12; 
    Episode: 02; Filename: Law & Order: Whatever.S11E02.Shit:It.Went.Down.X264-DIMENSION.mkv;""")
        self.assertEqual(data['name'], u'Law & Order: Whatever')
        self.assertEqual(data['title'], u'Shit: it went down')
        self.assertEqual(data['season'], u'12')
        self.assertEqual(data['episode'], u'02')
        self.assertEqual(data['filename'], u'Law & Order: Whatever.S11E02.Shit:It.Went.Down.X264-DIMENSION.mkv')
        self.assertEqual(data['quality'], u'sd')

    def test_episode_extraction_with_two_colons_in_name(self):
        data = extract_metadata(u"""Show Name:Law & Order:: Whatever; Show Title: Shit: it went down; Season: 12; 
    Episode: 02; Filename: Law & Order: Whatever.S11E02.Shit:It.Went.Down.X264-DIMENSION.mkv;""")
        self.assertEqual(data['name'], u'Law & Order:: Whatever')
        self.assertEqual(data['title'], u'Shit: it went down')
        self.assertEqual(data['season'], u'12')
        self.assertEqual(data['episode'], u'02')
        self.assertEqual(data['filename'], u'Law & Order: Whatever.S11E02.Shit:It.Went.Down.X264-DIMENSION.mkv')
        self.assertEqual(data['quality'], u'sd')
