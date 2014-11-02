# Colby's Basic Blog

_Note: This is not quite ready for production. Working on an admin interface in the near future._

This basic blog template includes:

1. Posts
2. Categories
3. Tags
4. Feeds
5. Basic Templates
6. Optional comments via Disqus

Version: 0.2.1

This is set up to work with [cp-project-template](https://github.com/colbypalmer/cp-project-template "CP Project Template") by the same author.

Installation
-----------

`pip install http://github.com/colbypalmer/django-cp-blog/dist/django-cp-blog-0.01a.tar.gz`


Quick start
-----------

1. Add "grappelli" to the beginning of your INSTALLED_APPS and "blog", "epiceditor", "taggit", and "taggit-tags" to the end:

    INSTALLED_APPS = (
        'grappelli',
        ... OTHER SETTINGS ...
        'blog',
        'epiceditor',
        'taggit',
        'taggit_templatetags',
    )

2. To use with Disqus comment integration, add `'DISQUS_SHORTNAME' = 'xxxxx'` to your settings.py.

3. Include the blog URLconf in your project urls.py like this::

    `url(r'^blog/', include('blog.urls')),`

4. Run `python manage.py migrate` to create the blog models.

5. Start the development server and visit http://127.0.0.1:8000/admin/blog/blogentry/
   to create a blog entry (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/blog/ to see your blog.


TODO: Document OpenGraph tags and location of base.html
