from django import template
from blog.models import BlogEntry, BlogCategory

register = template.Library()


@register.inclusion_tag("blog/_sidebar.html")
def get_blog_sidebar():
    recent = BlogEntry.active_objects.filter(status='2').order_by('-entry_date')[:10]
    categories = BlogCategory.objects.all().order_by('title')
    popular = BlogEntry.active_objects.filter(status='2').order_by('-view_count')[:10]
    return {
        'recent': recent,
        'categories': categories,
        'popular': popular
    }