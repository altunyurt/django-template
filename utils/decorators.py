# ~*~ coding:utf-8 ~*~

from django.conf import settings
from django.contrib.sites.models import Site
from utils.helpers import reverse_lazy
from django import http
import logging
logger = logging.getLogger(__name__)


class _requires_something(object):
    def __init__(self, retval=None):
        self.retval = retval

    def control_seq(self, f, request, *args, **kwargs):
        raise Exception(u'Bu kisim request kontrolu icermelidir')

    def __call__(self, view_func):
        def wrapped_func(request, *args, **kwargs):
            return self.control_seq(view_func, request, *args, **kwargs)
        return wrapped_func


class requires_nameless(_requires_something):
    def control_seq(self, f, request, *args, **kwargs):
        logger.debug('nameless')
        if request.user.username not in ('', None):
            return http.HttpResponseRedirect(self.retval)
        return f(request, *args, **kwargs)


class requires_username(_requires_something):
    def control_seq(self, f, request, *args, **kwargs):
        logger.debug('username')
        if request.user.username in ('', None):
            return http.HttpResponseRedirect(self.retval)
        return f(request, *args, **kwargs)


class requires_anonymous(_requires_something):
    ''' kullanici hesabi login edilmisse bu kisma erisemesin'''
    def control_seq(self, f, request, *args, **kwargs):
        logger.debug('anonymous')
        if request.user is not None and request.user.is_authenticated():
            return http.HttpResponseRedirect(self.retval)
        return f(request, *args, **kwargs)


class requires_activation(_requires_something):
    ''' kullanici hesabi aktif degilse yonlendirilsin'''
    def control_seq(self, f, request, *args, **kwargs):
        logger.debug('active')
        if request.user is not None and not request.user.is_active:
            return http.HttpResponseRedirect(self.retval)
        return f(request, *args, **kwargs)


class requires_admin(_requires_something):
    ''' kisi admin olmali '''
    def control_seq(self, f, request, *args, **kwargs):
        logger.debug('admin')
        if not request.user.is_superuser:
            return http.HttpResponseRedirect(self.retval)
        return f(request, *args, **kwargs)


class requires_staff(_requires_something):
    ''' admin degil ama admin arayzu kullanicisi olmali'''
    def control_seq(self, f, request, *args, **kwargs):
        logger.debug('staff')
        if not request.user.is_staff:
            return http.HttpResponseRedirect(self.retval)
        return f(request, *args, **kwargs)


class requires_post(_requires_something):
    ''' bu viewe post ile gelinmeli'''
    def control_seq(self, f, request, *args, **kwargs):
        logger.debug('post')
        if request.method != 'POST':
            return http.HttpResponseBadRequest('POST required')
        return f(request, *args, **kwargs)


class requires_ajax(_requires_something):
    ''' bu viewe ajax ile gelinmeli'''
    def control_seq(self, f, request, *args, **kwargs):
        logger.debug('ajax')
        if not request.is_ajax():
            return http.HttpResponseBadRequest('Ajax required')
        return f(request, *args, **kwargs)


class requires_secure(_requires_something):
    ''' guvenli baglanti yapilmali '''
    def control_seq(self, f, request, *args, **kwargs):

        logger.debug('secure')
        if settings.LOCAL or 'HTTP_X_FORWARDED_PROTOCOL' in request.META:
            return f(request, *args, **kwargs)

        site_address = Site.objects.get_current().domain
        return http.HttpResponseRedirect('https://%s%s' % (site_address, request.get_full_path()))


class requires_login(_requires_something):
    def control_seq(self, f, request, *args, **kwargs):
        logger.debug('login')
        if request.user.is_authenticated():
            return f(request, *args, **kwargs)
        response = http.HttpResponseRedirect(self.retval)
        ''' login yonlendirmelerinde next gitmek istedigi adres olmali '''
        response.set_cookie('next', request.path)
        return response


class requires_perms(_requires_something):
    def __init__(self, perms=[], redirect_to='/'):
        self.permissions = perms
        super(requires_perms, self).__init__(redirect_to)

    def control_seq(self, f, request, *args, **kwargs):
        logger.debug('perms')
        if request.user.has_perms(self.permissions):
            return f(request, *args, **kwargs)
        raise http.Http404()


### testing

try:
    if 'devserver' not in settings.INSTALLED_APPS:
        raise ImportError
    from devserver.modules.profile import devserver_profile
except ImportError:
    from functools import wraps
    class devserver_profile(object):
        def __init__(self, *args, **kwargs):
            pass
        def __call__(self, func):
            def nothing(*args, **kwargs):
                return func(*args, **kwargs)
            return wraps(func)(nothing)
