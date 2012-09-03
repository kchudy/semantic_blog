import urllib
import urllib2
from rdflib.graph import Graph
from rdflib.term import URIRef
from semantic_blog import settings
from semantic_blog.models import Enhancement, Entity, Tag

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

    entities = dict()
    enhancements = list()

    for subject in subjects:
        is_enhancement = get_first(g.triples((subject, predicate_type, URIRef('http://fise.iks-project.eu/ontology/Enhancement'))))

        if is_enhancement:
            enhancement = Enhancement()

            enhancement.value = get_first(g.objects(subject=subject, predicate=predicate_name))

            if not enhancement.value:
                enhancement.value = get_first(g.objects(subject=subject, predicate=predicate_entity_label))

            if enhancement.value:
                enhancement.entity_name = get_first(g.objects(subject=subject, predicate=predicate_entity_ref))

                enhancement.save()
                enhancements.append(enhancement)
        else:
            entity = Entity()
            entity.save()
            tags = map(save_tag, g.objects(subject=subject, predicate=predicate_resource))
            entity.tags = tags
            entity.comment = get_first(g.objects(subject=subject, predicate=predicate_comment))

            entity.save()

            entities[subject] = entity

    for enhancement in enhancements:
        if enhancement.entity_name:
            enhancement.entity = entities[enhancement.entity_name]
            enhancement.save()

#    sorted(enhancements, key=lambda x: x.name)

    return enhancements

def save_tag(value):
    return Tag.objects.get_or_create(value=str(value))[0]


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
