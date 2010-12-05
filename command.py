from feedparser import parse
from scraper import extract_metadata
from settings import get_settings
from persistence import TVShow, Session


def main():
    settings = get_settings()
    session = Session()
    feeds = settings.get('main', 'feeds').split()
    for feed_url in feeds:
        feed = parse(feed_url)
        for entry in feed.entries:
            data = extract_metadata(entry.description)
            try:
                data['torrent_url'] = entry.enclosures[0]['href']
            except (IndexError, KeyError):
                print "No torrent found for %(name)s" % data
            show = TVShow(**data)
            if session.query(TVShow).filter(TVShow.name==show.name).\
                filter(TVShow.season==show.season).\
                filter(TVShow.episode==show.episode).\
                filter(TVShow.quality==show.quality).count() > 0:
                continue
            session.add(show)
            print "Added %(name)s in %(quality)s" % show.__dict__ 
    
    session.commit()