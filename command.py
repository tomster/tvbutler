from os import mkdir, path
import ConfigParser
from shutil import copy
from feedparser import parse
from scraper import extract_metadata

CONFIG_PATH = path.expanduser('~/.tvbutler')

def get_settings():
    settings_path = path.join(CONFIG_PATH, 'config')
    if not path.exists(CONFIG_PATH):
        mkdir(CONFIG_PATH, 0700)
        default_settings_path = path.join(path.dirname(path.abspath(__file__)), 'config-sample.ini')
        copy(default_settings_path, settings_path)
        print "No feeds specified. Add them to %s and try again." % settings_path
        exit()
    config = ConfigParser.ConfigParser()
    config.read(settings_path)
    return config

def main():
    settings = get_settings()
    feeds = settings.get('main', 'feeds').split()
    for feed_url in feeds:
        feed = parse(feed_url)
        for entry in feed.entries:
            data = extract_metadata(entry.description)
            print "%(name)s in %(quality)s" % data

