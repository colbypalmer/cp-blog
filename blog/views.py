from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.http import Http404
from blog.models import BlogEntry, BlogCategory
from blog.search import *
from taggit.models import Tag, TaggedItem
import time
from calendar import month_name


def blog_list(request):
    entries = BlogEntry.active_objects.all().order_by('-entry_date')
    paginator = Paginator(entries, 5)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1
    try:
        entries = paginator.page(page)
    except (InvalidPage, EmptyPage):
        entries = paginator.page(paginator.num_pages)
    return render_to_response('blog/blog_list.html', dict(entries=entries, page_title="Blog", months=mkmonth_lst()),
                              context_instance=RequestContext(request))


def blog_detail(request, slug):
    slug_str = str(slug)
    entry = get_object_or_404(BlogEntry, slug=slug_str)
    entry.increment_count()
    return render_to_response('blog/blog_detail.html',
                              {'entry': entry, 'page_title': entry.title, 'months': mkmonth_lst()},
                              context_instance=RequestContext(request))


def blog_archive_date(request):
    return render_to_response('blog/blog_archive_date.html',
                              {'page_title': 'Blog Entries by Date', 'months': mkmonth_lst()},
                              context_instance=RequestContext(request))


def blog_archive_title(request):
    entries = BlogEntry.active_objects.all().order_by('-entry_date')
    return render_to_response('blog/blog_archive_title.html',
                              {'entries': entries, 'page_title': 'Blog Entries by Title'},
                              context_instance=RequestContext(request))


def blog_entries_by_category(request, slug):
    slug_str = str(slug)
    category = BlogCategory.objects.filter(slug=slug_str)
    entries = BlogEntry.active_objects.filter(category=category).order_by('-entry_date')
    paginator = Paginator(entries, 5)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1
    try:
        entries = paginator.page(page)
    except (InvalidPage, EmptyPage):
        entries = paginator.page(paginator.num_pages)

    return render_to_response('blog/blog_list.html', {'entries': entries, 'category': category[0].title,
                                                      'page_title': 'Entries by category "%s"' % category[0].title,
                                                      'months': mkmonth_lst()},
                              context_instance=RequestContext(request))


def blog_tags(request):
    return render_to_response("blog/blog_tags.html", {'page_title': 'Tags for this blog', 'months': mkmonth_lst()},
                              context_instance=RequestContext(request))


def blog_search(request):
    query_string = ''
    matches = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title', 'description', 'body', 'tags'])
        entries = BlogEntry.active_objects.filter(entry_query) or None
        try:
            paginator = Paginator(entries, 5)
            try:
                page = int(request.GET.get("page", '1'))
            except ValueError:
                page = 1
            try:
                entries = paginator.page(page)
            except (InvalidPage, EmptyPage):
                entries = paginator.page(paginator.num_pages)
        except TypeError:
            pass
        return render_to_response('blog/blog_list.html', dict(entries=entries, query_string=query_string,
                                                              page_title='Search Blog for "%s"' % query_string),
                                  context_instance=RequestContext(request))
    else:
        raise Http404


def blog_entries_by_tag(request, tag, object_id=None, page=1):
    page_title = 'Entries with tag "%s"' % tag
    try:
        query_tag = Tag.objects.get(name=tag)
        entries = TaggedItem.objects.get_by_model(BlogEntry, query_tag)
        entries = entries.order_by('-entry_date')
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
    return render_to_response("blog/blog_list.html",
                              dict(tag=tag, entries=entries, page_title=page_title, months=mkmonth_lst()),
                              context_instance=RequestContext(request))


def mkmonth_lst():
    """Make a list of months to show archive links."""

    if not BlogEntry.active_objects.count(): return []

    # set up vars
    year, month = time.localtime()[:2]
    first = BlogEntry.active_objects.order_by("entry_date")[0]
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


def month(request, year, month):
    """Monthly archive."""
    entries = BlogEntry.active_objects.filter(entry_date__year=year, entry_date__month=month)
    paginator = Paginator(entries, 5)
    page_title = 'Entries from %s, %s' % (month, year)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1
    try:
        entries = paginator.page(page)
    except (InvalidPage, EmptyPage):
        entries = paginator.page(paginator.num_pages)
    return render_to_response("blog/blog_list.html",
                              dict(entries=entries, page_title=page_title, months=mkmonth_lst(), archive=True),
                              context_instance=RequestContext(request))