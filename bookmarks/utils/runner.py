from logan.runner import run_app

import base64
import datetime
import os

KEY_LENGTH = 40

CONFIG_TEMPLATE = """import os

SECRET_KEY = %(default_key)r

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, 'database.db'),  # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")

STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# Please input your api keys below
BOOKMARKS_ZEMANTA_API_KEY = ''
BOOKMARKS_DIFFBOT_API_KEY = ''
"""


def generate_settings():
    """
    This command is run when ``default_path`` doesn't exist, or ``init`` is
    run and returns a string representing the default data to put into their
    settings file.
    """
    output = CONFIG_TEMPLATE % dict(
        default_key=base64.b64encode(os.urandom(KEY_LENGTH)),
    )

    return output


def main():
    run_app(
        project='mezzanine-bookmarks',
        default_settings='bookmarks.site.settings',
		default_config_path='~/.bookmarks/bookmarks.conf.py',
        settings_initializer=generate_settings,
        settings_envvar='BOOKMARKS_CONF',
    )

if __name__ == '__main__':
    main()
