# Colby's Basic Blog

_Note: This is not quite ready for production. Working on an admin interface in the near future._

This basic blog template includes:

1. Posts
2. Categories
3. Tags
4. Feeds
5. Basic Templates

Version: 0.01a

This is set up to work with [cp-project-template](https://github.com/colbypalmer/cp-project-template "CP Project Template") by the same author.


Quick start
-----------

1. Add "grappelli" to the beginning of your INSTALLED_APPS and "blog", "taggit", and "taggit-tags" to the end:

    INSTALLED_APPS = (
        'grappelli',
        ... OTHER SETTINGS ...
        'blog',
        'taggit',
        'taggit_templatetags',
    )

2. Include the blog URLconf in your project urls.py like this::

    `url(r'^blog/', include('blog.urls')),`

3. Run `python manage.py migrate` to create the blog models.

4. Start the development server and visit http://127.0.0.1:8000/admin/blog/blogentry/
   to create a blog entry (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/blog/ to see your blog.