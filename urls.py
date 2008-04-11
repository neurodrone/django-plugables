from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib import admin


# URL Patterns
urlpatterns = patterns('',
    
    # Nuts and Bolts
    (r'^', include('projects.urls')),
    
    # Blog
    (r'^blog/', include('blog.urls')),
    
    # Contact Form / About
    (r'^about/', include('contact_form.urls')),
    
    # Administration
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ('^admin/(.*)', admin.site.root),
    
)
