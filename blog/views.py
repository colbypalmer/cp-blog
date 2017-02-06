from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, View

from blog.models import BlogEntry, BlogCategory
from blog.search import *
from taggit.models import Tag, TaggedItem
import time
from calendar import month_name


class BlogListView(TemplateView):

    template_name = 'blog/blog_list.html'

    def get_context_data(self, **kwargs):

        if hasattr(settings, 'DISQUS_SHORTNAME'):
            disqus_shortname = settings.DISQUS_SHORTNAME
        else:
            disqus_shortname = None

        if self.request.user.is_staff:
            entries = BlogEntry.active_objects.all().order_by('-entry_date')
        else:
            entries = BlogEntry.active_objects.filter(status="2").order_by('-entry_date')
        paginator = Paginator(entries, 5)
        try:
            page = int(self.request.GET.get("page", '1'))
        except ValueError:
            page = 1
        try:
            entries = paginator.page(page)
        except (InvalidPage, EmptyPage):
            entries = paginator.page(paginator.num_pages)

        return dict(entries=entries, page_title="Blog", months=mkmonth_lst(), disqus_shortname=disqus_shortname)


class BlogDetailView(TemplateView):

    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        if hasattr(settings, 'DISQUS_SHORTNAME'):
            disqus_shortname = settings.DISQUS_SHORTNAME
        else:
            disqus_shortname = None

        if self.request.user.is_staff:
            entry = get_object_or_404(BlogEntry, slug=self.kwargs['slug'])
        else:
            entry = get_object_or_404(BlogEntry, slug=self.kwargs['slug'], status='2')
            entry.increment_count()

        return dict(entry=entry, page_title=entry.title, months=mkmonth_lst(), disqus_shortname=disqus_shortname)


class BlogArchiveDateView(TemplateView):

    template_name = 'blog/blog_archive_date.html'

    def get_context_data(self, **kwargs):
        return {'page_title': 'Blog Entries by Date', 'months': mkmonth_lst()}


class BlogArchiveTitleView(TemplateView):

    template_name = 'blog/blog_archive_title.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff:
            entries = BlogEntry.active_objects.all().order_by('-entry_date')
        else:
            entries = BlogEntry.active_objects.filter(status='2').order_by('-entry_date')

        return {'entries': entries, 'page_title': 'Blog Entries by Title'}


class BlogEntriesByCategoryView(TemplateView):

    template_name = 'blog/blog_list.html'

    def get_context_data(self, **kwargs):
        slug_str = str(self.kwargs['slug'])
        category = BlogCategory.objects.filter(slug=slug_str)

        if self.request.user.is_staff:
            entries = BlogEntry.active_objects.filter(category=category).order_by('-entry_date')
        else:
            entries = BlogEntry.active_objects.filter(category=category, status='2').order_by('-entry_date')

        paginator = Paginator(entries, 5)
        try:
            page = int(self.request.GET.get("page", '1'))
        except ValueError:
            page = 1
        try:
            entries = paginator.page(page)
        except (InvalidPage, EmptyPage):
            entries = paginator.page(paginator.num_pages)

        return {'entries': entries, 'category': category[0].title, 'page_title': 'Entries by category "%s"' % category[0].title, 'months': mkmonth_lst()}


class BlogTagsView(TemplateView):

    template_name = 'blog/blog_tags.html'

    def get_context_data(self, **kwargs):
        return {'page_title': 'Tags for this blog', 'months': mkmonth_lst()}


class BlogSearchView(TemplateView):

    template_name = 'blog/blog_list.html'

    def get_context_data(self, **kwargs):
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            entry_query = get_query(query_string, ['title', 'description', 'body'])
            if self.request.user.is_staff:
                entries = BlogEntry.active_objects.filter(entry_query) or None
            else:
                entries = BlogEntry.active_objects.filter(status='2').filter(entry_query) or None
            try:
                paginator = Paginator(entries, 5)
                try:
                    page = int(self.request.GET.get("page", '1'))
                except ValueError:
                    page = 1
                try:
                    entries = paginator.page(page)
                except (InvalidPage, EmptyPage):
                    entries = paginator.page(paginator.num_pages)
            except TypeError:
                pass
            return dict(entries=entries, query_string=query_string, page_title='Search Blog for "%s"' % query_string)
        else:
            raise Http404


# def blog_entries_by_tag(request, tag, object_id=None, page=1):

class BlogEntriesByTagView(TemplateView):

    template_name = 'blog/blog_list.html'

    def get_context_data(self, **kwargs):

        try:
            tag = Tag.objects.get(name=self.kwargs['tag'])

            if self.request.user.is_staff:
                entries = BlogEntry.objects.filter(tags__name__in=[tag]).order_by('-entry_date')
            else:
                entries = BlogEntry.objects.filter(status='2').filter(tags__name__in=[tag]).order_by('-entry_date')

            paginator = Paginator(entries, 5)
            try:
                page = int(request.GET.get("page", '1'))
            except ValueError:
                page = 1
            try:
                entries = paginator.page(page)
            except (InvalidPage, EmptyPage):
                entries = paginator.page(paginator.num_pages)
        except Tag.DoesNotExist:
            entries = None
            tag = ''
        page_title = 'Entries with tag "%s"' % tag
        return dict(tag=tag, entries=entries, page_title=page_title, months=mkmonth_lst())


def mkmonth_lst():
    """Make a list of months to show archive links."""

    if not BlogEntry.active_objects.count():
        return []

    # set up vars
    year, month = time.localtime()[:2]
    first = BlogEntry.active_objects.filter(status='2').order_by("entry_date")[0]
    fyear = first.entry_date.year
    fmonth = first.entry_date.month
    months = []

    # loop over years and months
    for y in range(year, fyear - 1, -1):
        start, end = 12, 0
        if y == year: start = month
        if y == fyear: end = fmonth - 1

        for m in range(start, end, -1):
            posts = BlogEntry.active_objects.filter(entry_date__year=y, entry_date__month=m)
            if posts.count(): months.append((y, m, month_name[m]))
    return months


class BlogMonthView(TemplateView):
    """Monthly archive."""

    template_name = 'blog/blog_list.html'

    def get_context_data(self, **kwargs):

        year = self.kwargs['year']
        month = self.kwargs['month']

        if self.request.user.is_staff:
            entries = BlogEntry.active_objects.filter(entry_date__year=year, entry_date__month=month)
        else:
            entries = BlogEntry.active_objects.filter(status='2', entry_date__year=year, entry_date__month=month)
        paginator = Paginator(entries, 5)
        page_title = 'Entries from %s, %s' % (month, year)
        try:
            page = int(self.request.GET.get("page", '1'))
        except ValueError:
            page = 1
        try:
            entries = paginator.page(page)
        except (InvalidPage, EmptyPage):
            entries = paginator.page(paginator.num_pages)
        return dict(entries=entries, page_title=page_title, months=mkmonth_lst(), archive=True)
