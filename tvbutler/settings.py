import logging
from os import mkdir, path
import ConfigParser
from shutil import copy

CONFIG_PATH = path.expanduser('~/.tvbutler')
DB_URL = 'sqlite:///%s' % path.join(CONFIG_PATH, 'database.db')
log = logging.getLogger('tvbutler')

settings_path = path.join(CONFIG_PATH, 'config')
if not path.exists(CONFIG_PATH):
    mkdir(CONFIG_PATH, 0700)
    default_settings_path = path.join(path.dirname(path.abspath(__file__)), 'config-sample.ini')
    copy(default_settings_path, settings_path)
    print "No feeds specified. Add them to %s and try again." % settings_path
    exit()

settings = ConfigParser.ConfigParser()
settings.read(settings_path)

logfile = logging.FileHandler(path.join(CONFIG_PATH, 'log'))
logfile.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
log.addHandler(logfile)
console = logging.StreamHandler()
console.setFormatter(logfile.setFormatter(logging.Formatter('%(message)s')))
log.addHandler(console)
log.setLevel(logging.INFO)

def settings_get(name, default=None, section='main'):
    if settings.has_option(section, name):
        return settings.get(section, name)
    else:
        return default
