import unittest
from scraper import extract_metadata

class TestScraper(unittest.TestCase):

    def test_episode_extraction(self):
        show, season, episode_number, episode_title, quality =\
            extract_metadata(u"""Show Name:The Daily Show with Jon Stewart; 
                Show Title: Justin Timberlake; Season: 2010; Episode: 09.30; 
                Filename: the.daily.show.2010.09.30.hdtv.xvid-fqm.avi;""")
        self.assertEqual(show, u'The Daily Show with Jon Stewart')
