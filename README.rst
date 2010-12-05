tvbutler reads RSS feeds from http://tvtorrents.com and downloads torrents of new episodes for you in your preferred quality (but is smart enough to fallback to non-HD versions, if available).

Configuration
=============

The configuration lives in `~/.tvbutler/config`::

  [main]
  download_dir=~/Downloads/
  # one of sd, 720p, 1080p
  preferred_quality=720p
  
  # one per line, indented
  feeds =
      http://www.tvtorrents.com/mytaggedRSS?digest=xxxxx
      http://www.tvtorrents.com/mydownloadRSS?digest=xxxx

Usage
=====

tvbutler is designed to work as a crontab or launchd entry. Called without any parameters it will download all given feeds, try to identify shows and then figure out which episodes are available in which quality. It then downloads the torrent files into the given target directory (which typically will be 'watched' by a torrent client).
