from django.conf.urls import url
from .feeds import LatestEntriesRssFeed, LatestEntriesAtomFeed
from .views import BlogListView, BlogDetailView, BlogTagsView, BlogSearchView, BlogArchiveDateView, BlogArchiveTitleView, \
    BlogEntriesByCategoryView, BlogEntriesByTagView, BlogMonthView

urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='blog'),
    url(r'^rss/$', LatestEntriesRssFeed(), name='blog_rss'),
    url(r'^atom/$', LatestEntriesAtomFeed(), name='blog_atom'),
    url(r'^tags/$', BlogTagsView.as_view(), name='blog_tags'),
    url(r'^search/$', BlogSearchView.as_view(), name='blog_search'),
    url(r'^archive/date/$', BlogArchiveDateView.as_view(), name='blog_archive_date'),
    url(r'^archive/title/$', BlogArchiveTitleView.as_view(), name='blog_archive_title'),
    url(r'^month/(\d+)/(\d+)/$', BlogMonthView.as_view(), name='blog_month'),
    url(r'^(?P<slug>[\w\._-]+)/$', BlogDetailView.as_view(), name='blog_detail'),
    url(r'^category/(?P<slug>[\w\._-]+)/$', BlogEntriesByCategoryView.as_view(), name='blog_entries_by_category'),
    url(r'^tag/(?P<tag>[-_A-Za-z0-9]+)/$', BlogEntriesByTagView.as_view(), name='blog_entries_by_tag'),
]
