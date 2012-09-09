from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    value = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('semantic_blog.views.view_tag', (), {
            'tag_id': str(self.id)
        })

    def get_articles(self):
        return Article.objects.filter(tags__pk=self.pk)

    def __unicode__(self):
        return self.value

    def __eq__(self, other):
        return isinstance(other, Tag) and self.value == other.value

    def __hash__(self):
        return self.value.__hash__()

    def __ne__(self, other):
        return not self.__eq__(other)

class Enhancement(models.Model):
    value = models.CharField(max_length=20000)
    comment = models.CharField(max_length=20000, null=True)

    def __eq__(self, other):
        return isinstance(other, Enhancement) and self.value == other.value

    def __hash__(self):
        return self.value.__hash__()

    def __ne__(self, other):
        return not self.__eq__(other)


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=20000)
    enhancements = models.ManyToManyField(Enhancement)
    tags = models.ManyToManyField(Tag)

    @models.permalink
    def get_absolute_url(self):
        return ('semantic_blog.views.view_article', (), {
            'article_id': str(self.id)
        })

    def __unicode__(self):
        return self.title

    def get_enhancements(self):
        return sorted(self.enhancements.all(), key=lambda x: x.value)

    def get_tags(self):
        return sorted(self.tags.all(), key=lambda x: x.value)

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

