from feedparser import parse
from optparse import OptionParser
from os import path
from urllib import urlretrieve

from scraper import extract_metadata
from settings import settings, log
from persistence import TVShow, Session

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
    help="Read RSS from this file instead of the feeds specified"
    "in the config file.")


def main():
    session = Session()
    (options, args) = parser.parse_args()
    if options.filename is not None:
        feeds = [options.filename]
    else:
        feeds = settings.get('main', 'feeds').split()
    preferred_quality = settings.get('main', 'preferred_quality')
    log.info("Begin of run.")
    for feed_url in feeds:
        feed = parse(feed_url)
        log.info("Checking %s" % feed['feed']['subtitle'])
        for entry in feed.entries:
            data = extract_metadata(entry.description)
            try:
                data['torrent_url'] = entry.enclosures[0]['href']
            except (IndexError, KeyError):
                log.warning("No torrent found for %(name)s" % data)
            show = TVShow(**data)
            existing_qualities = session.query(TVShow).filter(TVShow.name==show.name).\
                filter(TVShow.season==show.season).\
                filter(TVShow.episode==show.episode)
            preferred_qualities = existing_qualities.\
                filter(TVShow.quality==preferred_quality)

            # nothing yet? then add unconditionally
            if existing_qualities.count()==0:
                session.add(show)
                log.info("Added %(name)s %(title)s in %(quality)s" % show.__dict__)
            # already in preferred quality?
            elif preferred_qualities.count() > 0:
                continue
            # update existing quality with this one:
            else:
                existing_quality = existing_qualities.one()
                if show.quality != existing_quality.quality:
                    session.delete(existing_quality)
                    session.add(show)
                    log.info("Updated %(name)s %(title)s to %(quality)s" % show.__dict__)
    
    torrent_download_dir = path.expanduser(settings.get('main', 'torrent_download_dir'))
    log.info("downloading torrents to %s" % torrent_download_dir)
    for show in session.query(TVShow).filter(TVShow.status==u'new'):
        torrent_path, result = urlretrieve(show.torrent_url, path.join(torrent_download_dir,
            "%s.torrent" % show.filename))
        if result.type == 'application/x-bittorrent':
            show.status = u'torrent_downloaded'
            log.info("Downloading torrent for %(name)s %(title)s in %(quality)s" % show.__dict__)
        else:
            log.error("Couldn't download %s" % show.torrent_url)

    session.commit()
    log.info("End of run.")
