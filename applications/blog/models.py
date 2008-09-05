from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google

from managers import *
from core.constants import MARKUP_CHOICES
from tagging.fields import TagField
from template_utils.markup import formatter
from typogrify.templatetags.typogrify import typogrify


class Entry(models.Model):
    """
    An ``Entry`` contains data pertainting to a specific topic. Entries are 
    tied together by tags to create topic groups.
    """
    
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3    
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
        
    # Dates
    published = models.DateTimeField('Date Published', default=datetime.now)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)
    
    # Meta
    author = models.ForeignKey(User)
    title = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField()
    
    # Categorization
    tags = TagField(help_text='Add tags for this entry (space separated).')
    
    # Content
    summary = models.TextField(help_text='Enter a brief summary of this blog entry.')
    body = models.TextField(help_text='Enter the main content of this entry.')
    
    # Pre-Processed Content
    summary_processed = models.TextField('Processed Summary', editable=False)
    body_processed = models.TextField('Processed Body', editable=False)
    
    # Options
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS, help_text='Select the status of this blog entry.')
    enable_comments = models.BooleanField('Comments?', default=True, help_text='Select \'True\' if you wish to enable visitors to comment on this entry.')
    
    # Mangers
    objects = LiveEntryManager()
    
    class Meta:
        get_latest_by = 'published'
        ordering = ['-published']
        verbose_name_plural = 'entries'
    
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('entry-detail', (), {
            'year'  : self.published.year, 
            'month' : self.published.strftime('%b').lower(), 
            'day'   : self.published.day, 
            'slug'  : self.slug
        })
    
    def _next_previous_helper(self, direction):
        return getattr(self, 'get_%s_by_published' % direction)(status__exact=self.LIVE_STATUS)
    
    def _process_markup(self):
        """
        Returns the entry with content elements processed by markup and typogrify.
        """
        self.summary_processed = typogrify(formatter(self.summary))
        self.body_processed = typogrify(formatter(self.body))
        return self
    
    def _get_tags(self):
        return Tag.objects.get_for_object(self)
    
    def _set_tags(self, tag_list):
        Tag.objects.update_tags(self, tag_list)
    
    def get_tags(self):
        return [value.strip(' ,') for value in self.tags.split()]
    
    @property
    def get_next(self):
        return self._next_previous_helper('next')
    
    @property
    def get_previous(self):
        return self._next_previous_helper('previous')
    
    def save(self):
        # Create or update the proper dates.
        if not self.id:
            self.created = datetime.now()
            self.updated = self.created
        else:
            self.updated = datetime.now()
        
        # Process markup language.
        self = self._process_markup()
        
        # Save this time, really.
        super(Entry, self).save()
        
        # Ping Google.
        try:
            ping_google()
        except Exception:
            pass
    
