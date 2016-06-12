# ~*~ coding:utf-8 ~*~

from django.contrib.sessions.middleware import SessionMiddleware as _SessionMiddleware
from django.utils.importlib import import_module
from django.conf import settings

import threading
_thread_locals = threading.local()

import logging
logger = logging.getLogger(__name__)

class SessionMiddleware(_SessionMiddleware):
    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, request.POST.get('sessionid', None))
        request.session = engine.SessionStore(session_key)


def get_current_request():
    return getattr(_thread_locals, 'request', None)

def set_current_user(user):
    """Stores the logged in user serviced by this thread"""
    _thread_locals.user = user

def get_current_user():
    """query the information stored by ThreadLocals."""
    return getattr(_thread_locals, 'user', None)


def set_remote_ip(ipaddr):
    """Stores the remote IP address serviced by this thread"""
    _thread_locals.remote_ip = ipaddr


def get_remote_ip():
    """query the information stored by ThreadLocals."""
    return getattr(_thread_locals, 'remote_ip', None)


class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""

    def process_request(self, request):
        """Store certain data at every request."""
        set_current_user(getattr(request, 'user', None))
        set_remote_ip(request.META.get('REMOTE_ADDR', None))
        _thread_locals.request = request
