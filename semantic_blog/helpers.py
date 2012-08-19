import urllib
import urllib2
import rdflib
from semantic_blog import settings

def store_article_in_stanbol(article):
    url = settings.STANBOL_CONTENTHUB_STORE_URL % {'item_id' : article.pk}
    headers = {'Content-Type' : 'text/plain'}

    values = {'data' : article.content}

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)

    html = response.read()

    print html

def get_article_meta_data(article_id):
    url = settings.STANBOL_CONTENTHUB_GET_META_URL % {'item_id' : article_id}
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)

    rdf = response.read()

    g = rdflib.Graph()
    result = g.parse(data=rdf)
    print("graph has %s statements." % len(g))

    for subj, pred, obj in g:
        if (subj, pred, obj) not in g:
            raise Exception("It better be!")

    print result

