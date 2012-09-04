from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from semantic_blog import settings

urlpatterns = patterns('',
    (r'^$', 'semantic_blog.views.index'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^find', 'semantic_blog.views.find_content'),
    (r'^article/create$', 'semantic_blog.views.create_article'),
    (r'^article/(?P<article_id>\d+)$', 'semantic_blog.views.view_article'),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
