import urllib
import urllib2
from django.utils import simplejson
import rdflib
from rdflib.term import URIRef
from semantic_blog import settings
from semantic_blog.models import Enhancement, Entity

def get_article_enhancements(article):
    g = rdflib.Graph()

    g.parse(get_content_meta_rdf(article.content))

    entities = dict()

    for subject in g.subjects():
        if str(subject).startswith('http://dbpedia.org/resource/'):
            label = g.preferredLabel(subject=subject, lang='en')[0][1]

            for predicate, object in g.predicate_objects(subject=subject):
                enhancement = Enhancement()

                enhancement.predicate = predicate
                enhancement.object = object

                add_to_dict(entities, key=label, value=enhancement)

    return entities

def get_content_meta(content):
    url = settings.STANBOL_CONTENTHUB_GET_META_URL

    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Accept' : 'application/json',
        }

    values = {
        'content' : content,
        }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)

    response = urllib2.urlopen(req)

    return response

def get_content_meta_rdf(content):
    url = settings.STANBOL_CONTENTHUB_GET_META_URL

    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Accept' : 'application/rdf+xml',
        }

    values = {
        'content' : content,
        }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)

    response = urllib2.urlopen(req)

    return response

def add_to_dict(dict, key, value):
    if dict.has_key(key):
        dict[key].append(value)
    else:
        dict[key] = list()
        dict[key].append(value)

def to_unicode_str(value):
    return unicode(str(value), errors='ignore')