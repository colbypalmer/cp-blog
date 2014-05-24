SITE_URL = "http://project.com"
SITE_NAME = "Project Name"

COMMENTS_APP = 'threadedcomments' # for example
RECAPTCHA_PUBLIC_KEY = 'put-your-key-here'
RECAPTCHA_PRIVATE_KEY = 'put-your-key-here'

SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}

TAGGIT_TAGCLOUD_MIN = 1
TAGGIT_TAGCLOUD_MAX = 8

GRAPPELLI_ADMIN_TITLE = u'{} Administration'.format(SITE_NAME)

INSTALLED_APPS = (
    'grappelli', # this should go first in the entire list
    'blog',
)