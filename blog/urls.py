from django.conf.urls import url
from blog.feeds import LatestEntriesRssFeed, LatestEntriesAtomFeed

urlpatterns = [
    url(r'^$', 'blog.views.blog_list', name='blog'),
    url(r'^rss/$', LatestEntriesRssFeed(), name='blog_rss'),
    url(r'^atom/$', LatestEntriesAtomFeed(), name='blog_atom'),
    url(r'^tags/$', 'blog.views.blog_tags', name='blog_tags'),
    url(r'^search/$', 'blog.views.blog_search', name='blog_search'),
    url(r'^archive/date/$', 'blog.views.blog_archive_date', name='blog_archive_date'),
    url(r'^archive/title/$', 'blog.views.blog_archive_title', name='blog_archive_title'),
    url(r'^month/(\d+)/(\d+)/$', 'blog.views.month', name='blog_month'),
    url(r'^(?P<slug>[\w\._-]+)/$', 'blog.views.blog_detail', name='blog_detail'),
    url(r'^category/(?P<slug>[\w\._-]+)/$', 'blog.views.blog_entries_by_category', name='blog_entries_by_category'),
    url(r'^tag/(?P<tag>[-_A-Za-z0-9]+)/$', 'blog.views.blog_entries_by_tag', name='blog_entries_by_tag'),
]
