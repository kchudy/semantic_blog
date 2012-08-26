from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=20000)
    meta = models.CharField(max_length=20000, null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('semantic_blog.views.view_article', (), {
            'article_id': str(self.id)
        })

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    def get_display_name(self):
        return self.first_name + ' ' + self.last_name
        
    def __unicode__(self):
        return self.get_display_name()

class UserArticleConnection(models.Model):
    AUTHOR = 0
    FAN = 1
    HATER = 2
    READER = 3

    user = models.ForeignKey(UserProfile)
    article = models.ForeignKey(Article)
    connection = models.IntegerField()

class Enhancement:
    pass

class Entity:
    pass
