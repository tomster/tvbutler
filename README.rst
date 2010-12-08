tvbutler reads RSS feeds from http://tvtorrents.com and downloads torrents of new episodes for you in your preferred quality (but is smart enough to fallback to non-HD versions, if available).

Installation and Usage
======================

Just use `easy_install` like so::

  easy_install tvbutler

Alternatively, download the archive, expand it and run::

  python setup.py install

This will install a command line executable ``tvbutler``. It's designed to work as a ``crontab`` or ``launchd`` entry: called without any parameters it will download all given feeds, try to identify shows and then figure out which episodes are available in which quality.

It then downloads the torrent files into the given target directory (which typically will be 'watched' by a torrent client).

tvbutler keeps a log of its activities in `~/.tvbutler/log` and a (sqlite) database of known shows and episodes in `~/.tvbutler/database.db`

Configuration
=============

The configuration lives in `~/.tvbutler/config`, the installer places a sample configuration and should be pretty self-explanatory::

  [main]
  download_dir=~/Downloads/
  # one of sd, 720p, 1080p
  preferred_quality=720p
  
  # one per line, indented
  feeds =
      http://www.tvtorrents.com/mytaggedRSS?digest=xxxxx
      http://www.tvtorrents.com/mydownloadRSS?digest=xxxx

Since tvbutler is aimed at downloading new episodes of currently running shows as they are released, it excludes by default all torrents it recognizes as archives of entire seasons. It does so by excluding all torrents whose description matches a regular expression, which is configurable via the config file::

  global_exclude_regex=(all.month|month.of|season[\s\d]*complete)

TODO
====

 * archive or delete files older than `n` days (perhaps base decision on tag)
 * remove torrents from transmission that have reached their seeding limit
