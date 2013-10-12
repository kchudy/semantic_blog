from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from semantic_blog import settings

urlpatterns = patterns(
    '',
    (r'^$', 'semantic_blog.views.index'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^find/', 'semantic_blog.views.find_content'),
    (r'^articles/$', 'semantic_blog.views.create_article'),
    (r'^articles/(?P<article_id>\d+)$', 'semantic_blog.views.view_article'),
    (r'^tags/$', 'semantic_blog.views.tag_list'),
    (r'^tags/(?P<tag_id>\d+)/$', 'semantic_blog.views.view_tag'),
    (r'^static/(?P<path>.*)/$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
