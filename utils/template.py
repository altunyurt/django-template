# ~*~ encoding: utf-8 ~*~

from datetime import datetime
from .decorators import reverse_lazy
from django import http
from itertools import ifilter
import urllib
from jinja2 import Environment
from django.core.urlresolvers import reverse
from utils.helpers import slugify


def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.lists():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v = v.decode('utf8')
        elif isinstance(v, list):
            _v = []
            for item in v:
                if isinstance(item, unicode):
                    item = item.encode('utf8')
                elif isinstance(item, str):
                    # Must be encoded in UTF-8
                    item = item.decode('utf8')
                _v.append(item)
            v = _v
        out_dict[k] = v
    return out_dict


def make_uri(GET, key, val, append=False):
    """
        a=1&b=2&c=3 türü bir uri key: b, val: 8 için
        append = False durumunda a=1&b=8&c=3
        append = True durumunda a=1&b=2&b=8&c=3
    """
    _GET = http.QueryDict(GET) if isinstance(GET, basestring) else GET
    _uri = _GET.copy()
    _vals = _uri.getlist(key, [])

    if append:
        _vals.append(val)
    else:
        _vals = [val]

    _uri.setlist(key, set(_vals))

    _uri = encoded_dict(_uri)

    # urlencode ikinci parametre olmaksıızn []ları da quote ediyor
    # dict olmadan da multival kısımları teke indiriyor
    return "?%s" % urllib.urlencode(dict(_uri), doseq=True)


def trim_uri(GET, key, val=None, url_encode=True):
    """ bir uriden ilgili keyi çıkartoıyoruz """
    _uri = GET.copy()
    try:
        if not val:
            del _uri[key]
        else:
            _uri.setlist(key, filter(lambda x: x != val, _uri.getlist(key, [])))
    except KeyError:
        pass

    if _uri:
        if url_encode:
            return "?%s" % urllib.urlencode(dict(_uri), doseq=True)
        return _uri
    return "?"


def req_to_dict(GET, splitter="_", excludes=[]):
    d = {}
    for k in GET:
        if k in excludes:
            continue
        d[k] = {}

        for l in ifilter(lambda x: x.strip(), GET.getlist(k)):

            id, name = l.split(splitter)
            d[k].update({id: name})
    return d


def url_for(view_func, *args, **kwargs):
    return reverse_lazy(view_func, args=args, kwargs=kwargs)


# filters
def r_date(d):
    """%Y-%m-%d => %b %d, %Y
        string filter unicode dönmeli imiş
    """
    t = datetime.strptime(d, "%Y-%m-%d") if isinstance(d, basestring) else d
    return unicode(t.strftime("%b %d, %Y"))


def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url': reverse,
        'slugify': slugify
    })
    return env
