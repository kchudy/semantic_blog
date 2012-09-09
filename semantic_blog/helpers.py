import urllib
import urllib2
from rdflib.graph import Graph
from rdflib.term import URIRef
from semantic_blog import settings
from semantic_blog.models import Enhancement, Tag

def get_or_create_enhancement(dict, key):
    if not dict.has_key(key):
        dict[key] = Enhancement()

    return dict[key]

def get_article_enhancements(article):
    g = Graph()
    g.parse(get_content_meta_rdf(article.content))

    predicate_name = URIRef('http://fise.iks-project.eu/ontology/selected-text')
    predicate_entity_label = URIRef('http://fise.iks-project.eu/ontology/entity-label')
    predicate_resource = URIRef('http://purl.org/dc/terms/subject')
    predicate_comment = URIRef('http://www.w3.org/2000/01/rdf-schema#comment')
    predicate_entity_ref = URIRef('http://fise.iks-project.eu/ontology/entity-reference')
    predicate_type = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')

    subjects = set(g.subjects())

    enhancements = set()
    tags = set()

    for subject in subjects:
        is_enhancement = get_first(g.triples((subject, predicate_type, URIRef('http://fise.iks-project.eu/ontology/Enhancement'))))

        if is_enhancement:
            enhancement = Enhancement()

            value = get_first(g.objects(subject=subject, predicate=predicate_name))

            if not value:
                value = get_first(g.objects(subject=subject, predicate=predicate_entity_label))

            if value:
                # there are enhancements with no value - ignore them
                enhancement.value = value

                entity_name = get_first(g.objects(subject=subject, predicate=predicate_entity_ref))

                if entity_name:
                    enhancement.comment = get_first(g.objects(subject=entity_name, predicate=predicate_comment))
                    entity_tags = map(save_tag, g.objects(subject=entity_name, predicate=predicate_resource))

                    # TODO try some set operations
                    for tag in entity_tags:
                        tags.add(tag)

                # check if the set contains the richest enhancement
                if enhancement in enhancements and enhancement.comment:
                    enhancements.remove(enhancement)

                enhancements.add(enhancement)

#    sorted(enhancements, key=lambda x: x.name)

    for enhancement in enhancements:
        enhancement.save()

    return enhancements, tags

def get_tag_value(tag_raw):
    return urllib.unquote(str(tag_raw).replace('http://dbpedia.org/resource/Category:', '').replace('_', ' '))

def save_tag(value):
    tag_value = urllib.unquote(str(value).replace('http://dbpedia.org/resource/Category:', '').replace('_', ' '))
    return Tag.objects.get_or_create(value=tag_value, url=str(value))[0]


def get_content_meta_json(content):
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

def get_first(generator):
    try:
        return generator.next()
    except StopIteration:
        return False
