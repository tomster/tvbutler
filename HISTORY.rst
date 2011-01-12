0.1.b2 - Unreleased
===================

0.1.b1 - 2011-01-12
===================

* Documentation cleanup (thanks to `claytron <https://github.com/claytron>`_)
* Fix for shows with ':' in their name (thanks to `plambert <https://github.com/plambert>`_), fixes https://github.com/tomster/tvbutler/pull/5

0.1a5 - 2010-12-17
==================

* robustness fix (tvbutler would barf on some entries and stop processing the remaining entries)
* log to stdout, too to get instant feedback when calling tvbutler from console

0.1a4 - 2010-12-08
==================

* added global regular expression filter (defaults to skip archives of
  seasons)

  `UPGRADE NOTE`: add ``global_exclude_regex=(all.month|month.of|season[\s\d]*complete)``
  to the ``[main]`` section your existing config to activate this feature.

0.1a3 - 2010-12-05
==================

* added logging


0.1a2 - 2010-12-05
==================

Initial release (0.1a was nuked due to packaging foobar)
