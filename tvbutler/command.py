import re
import transmissionrpc
from feedparser import parse
from optparse import OptionParser
from os import path
from pkg_resources import get_distribution
from urllib import urlretrieve

from scraper import extract_metadata
from settings import settings_get, log
from persistence import TVShow, Session, migrations

parser = OptionParser(
    version="tvbutler %s" % get_distribution("tvbutler").version)
parser.add_option("-f", "--file", dest="filename",
    help="Read RSS from this file instead of the feeds specified"
    "in the config file.")
parser.add_option("-m", "--migrate", dest="migration_step",
    help="Migrate the database to the given target version")


def main():
    log.info("------------------------------------------------------------")
    session = Session()
    (options, args) = parser.parse_args()
    if options.filename is not None:
        feeds = [options.filename]
    else:
        feeds = settings_get('feeds').split()
    if options.migration_step is not None:
        migration_step = int(options.migration_step)
        log.info('Migrating show database to %d' % migration_step)
        migrations[migration_step]()
    preferred_quality = settings_get('preferred_quality')
    global_exclude_regex = settings_get('global_exclude_regex')
    if global_exclude_regex is not None:
        exclude_regex = re.compile(global_exclude_regex)
    else:
        exclude_regex = None

    for feed_url in feeds:
        feed = parse(feed_url)
        log.info("Checking %s" % feed['feed']['subtitle'])
        for entry in feed.entries:
            if (exclude_regex is not None and
                exclude_regex.search(entry.description.lower()) is not None):
                log.info("SKIP %s" % entry.description)
                continue
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
                log.info("FOUND %(name)s %(season)s %(episode)s in %(quality)s" % show.__dict__)
            # already in preferred quality?
            elif preferred_qualities.count() > 0:
                continue
            # update existing quality with this one:
            else:
                existing_quality = existing_qualities.one()
                if show.quality != existing_quality.quality:
                    session.delete(existing_quality)
                    session.add(show)
                    log.info("UPDATED %(name)s %(season)s %(episode)s to %(quality)s" % show.__dict__)
    
    transmission_host = settings_get('transmission_host', None)
    if transmission_host is not None:
        transmission_port = settings_get('transmission_port', 9091)
        transmission = transmissionrpc.Client(transmission_host,
            port=transmission_port)
        log.info("connected to transmission at %s:%s" % (transmission_host, transmission_port))
    else:
        torrent_download_dir = path.expanduser(settings_get('torrent_download_dir', None))
        log.info("downloading torrents to %s" % torrent_download_dir)
    for show in session.query(TVShow).filter(TVShow.status==u'new'):
        if transmission_host is None:
            torrent_path, result = urlretrieve(show.torrent_url, path.join(torrent_download_dir,
                "%s.torrent" % show.filename))
            if result.type == 'application/x-bittorrent':
                show.status = u'torrent_downloaded'
                log.info("DOWNLOAD %(name)s %(season)s %(episode)s in %(quality)s" % show.__dict__)
            else:
                log.error("Couldn't download %s" % show.torrent_url)
        else:
            try:
                torrent = transmission.add_uri(show.torrent_url).values()[0]
                show.transmission_hash = torrent.fields['hashString']
                show.status = u'torrent_downloaded'
                log.info("ADDED %(name)s %(season)s %(episode)s in %(quality)s" % show.__dict__)
            except transmissionrpc.error.TransmissionError:
                pass

    session.commit()
