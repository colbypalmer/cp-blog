import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from markdown import markdown
from positions import PositionField
from taggit.managers import TaggableManager
from utils.thumbs import ImageWithThumbsField


BLOG_ENTRY_STATUS = (
    ("1", "Closed"),
    ("2", "Public"),
    ("3", "Private"),
    ("4", "Expired"),
    ("5", "Draft"),
)


class BlogCategory(models.Model):
    """
    Categories for blog entries.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=80, unique=True, help_text=_(
        "a short version of the name consisting only of letters, numbers, underscores and hyphens."))
    active = models.BooleanField(default=True)
    position = PositionField()

    @models.permalink
    def get_absolute_url(self):
        return ('blog_category', (), {'blog_category_slug': self.slug})

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')


class ActiveEntryManager(models.Manager):
    def get_queryset(self):
        return super(ActiveEntryManager, self).get_queryset().filter(active=True)


class BlogEntry(models.Model):
    """
    Blog entry data.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=80, unique=True, help_text=_(
        "a short version of the name consisting only of letters, numbers, underscores and hyphens."))
    description = models.CharField(blank=True, max_length=255)
    body = models.TextField(blank=True)
    body_markdown = models.TextField(blank=True)
    image = ImageWithThumbsField(blank=True, upload_to='blog', sizes=((200, 300), (600, 900)))
    category = models.ForeignKey(BlogCategory, blank=True)
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=2, choices=BLOG_ENTRY_STATUS)
    author = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    comments_open = models.BooleanField(default=True)
    sticky = models.BooleanField(default=False)
    view_count = models.IntegerField(blank=True, null=True, default=0)
    entry_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, editable=True,
                                      default=datetime.datetime.now)
    edited_date = models.DateTimeField(blank=True, null=True, auto_now=True, auto_now_add=True, editable=True,
                                       default=datetime.datetime.now)
    old_date = models.IntegerField(blank=True, null=True, max_length=20)
    expiration_date = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()  # The default manager.
    active_objects = ActiveEntryManager()  # The active-and-processed-specific manager.

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Blog Entry')
        verbose_name_plural = _('Blog Entries')

    @property
    def status_display(self):
        choices = BLOG_ENTRY_STATUS
        for o in choices:
            if str(self.status) in o:
                return o[1]

    #    @models.permalink
    def get_absolute_url(self):
        #        return ('blog_entry', (), { 'blog_entry_slug': self.slug })
        return '/blog/%s/' % self.slug

    def increment_count(self):
        if not self.view_count:
            self.view_count = 0
        self.view_count += 1
        models.Model.save(self)

    def save(self, *args, **kwargs):
        if not self.entry_date:
            self.entry_date = datetime.datetime.now()
        self.body = markdown(self.body_markdown, ['codehilite'])
        super(BlogEntry, self).save(*args, **kwargs)
