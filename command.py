from feedparser import parse
from scraper import extract_metadata
from settings import get_settings


def main():
    settings = get_settings()
    feeds = settings.get('main', 'feeds').split()
    for feed_url in feeds:
        feed = parse(feed_url)
        for entry in feed.entries:
            data = extract_metadata(entry.description)
            try:
                data['torrent_url'] = entry.enclosures[0]['href']
            except (IndexError, KeyError):
                print "No torrent found for %(name)s" % data

