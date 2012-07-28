mezzanine-bookmarks 
===================

WARNING: mezzanine-bookmarks is under development.

mezzanine-bookmarks is a bookmark service built on Django and Mezzanine designed to be flexible and easy to use.
You could host it as a standalone bookmark service for multiple users. Or you could embed it into an existing mezzanine site.

Here is the feature list:

- Multiple User support
- Single User mode
- Use service from www.diffbot.com to extract main content from web page
- Use service from api.zemanta.com to generate suggested tags
- Store page content for future use

INSTALL
*******

EMBED INSTALL
-------------

mezzanine-bookmarks could be used as a django app::

	pip install mezzanine-bookmarks

Then add ``'bookmarks',`` to INSTALLED_APPS and add ``("^bookmarks/", include("bookmarks.urls")),`` to ``urls.py``.

STANDALONE INSTALL
------------------

mezzanine-bookmarks comes with a standalone mode which you could use run a bookmark service with it very quickly::

	virtualenv bookmarks
	source bookmarks/bin/activate
	pip install mezzanine-bookmarks
	pip install django-template-bootstrap
	bookmarks init
	vim ~/.bookmarks/bookmarks.conf.py # Add your own diffbot and zemanta api keys
	bookmarks syncdb
	bookmarks migrate
	bookmarks runserver

