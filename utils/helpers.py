# coding:utf-8

from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify as djslugify
from random import choice
from string import lowercase, digits, uppercase
from unidecode import unidecode
import exceptions as exc

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.utils.functional import lazy
    reverse_lazy = lazy(reverse, str)

import logging
logger = logging.getLogger(__name__)


def generate_random_string(max_length=5, pool=None):
    pool = pool or (lowercase + uppercase + digits)
    return "".join([choice(pool) for i in range(max_length)])


def paginate(objlist, numitems, pagenum, count=None):
    paginator = Paginator(objlist, numitems)
    if count is not None:
        ''' raw querylerde count'u disardan sagliyoruz. aksi halde len falan ile almak gerek ki
        bu da bellek dertleri yaratabilir.
        '''
        paginator._count = count

    # eğer olmayan bir sayfa istenmişse, mevcut son sayfayı dön
    return paginator.page(pagenum) if pagenum <= paginator.num_pages else paginator.page(paginator.num_pages)


def t_int(_str, default=0):
    ''' degeri integer'a cevir, ya da default degeri don'''
    try:
        return int(_str)
    except (exc.ValueError, exc.TypeError):
        pass
    return default


def get_int(request, param, default=None):
    return t_int(request.REQUEST.get(param), default)


def one_or_none(klass, *args, **kwargs):
    ''' sorgudan sonuc donerse ilk sonucu al, hata veya sifir sonuc durumunda None don'''
    objs = klass if not hasattr(klass, 'objects') else klass.objects
    flt = objs.filter(*args, **kwargs)
    return flt[0] if flt.exists() else None


def chunks(l, n):
    ''' listeyi n elemanli alt gruplara boluyoruz.
        orn: [1,2,3,4,5,6,7,8,9,0] -> [[1,2,3], [4,5,6], [7,8,9], [0]]
    '''
    for i in xrange(0, len(l), n):
        yield l[i:i+n]




def slugify(title):
    return djslugify(unidecode(title))


def concat(items, glue):
    """ bazen stringleri birleştirmek istiyorum ama bunların bazıları
    boş olabilir mi diye kontrol etmekten sıkılıyorum.
    örneğin: a, b, c yi "-" ile birleştireceğim
    ama mesela b boş ise, none ise a-c elde etmek istiyorum"""

    return glue.join(filter(lambda x: x, items))



