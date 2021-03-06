# ~*~ encoding: utf-8 ~*~

from datetime import date as dt_date
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.query import RawQuerySet
from django.db.models.signals import post_save, pre_save
from unidecode import unidecode
from utils.helpers import reverse, reverse_lazy, chunks
from utils.model_base import _Model, QuerySet, models
import os


class UserObjects(UserManager):
    attrs = {
        'full_name': "CONCAT(first_name, ' ', last_name)"
    }

    #def get_query_set(self):
    #    return super(UserObjects, self).get_query_set().extra( select=self.attrs)
    def get_query_set(self):
        """
            Eger bir class icinde queryset tanimi yapilmamissa ilk yuklemede patliyor.
            Asagidaki kontrol bunu engelliyor
        """
        if hasattr(self.model, 'QuerySet'):
            return self.model.QuerySet(self.model).extra(select=self.attrs)

        elif self.model._meta.fields:
            return QuerySet(self.model)

    def __getattr__(self, attr, *args):

        ''' ozel methodlari aramaya kalktindiga maximum recursion problemi doguyor '''
        if attr.startswith("_"):  # or at least "__"
            raise AttributeError
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)


class User(AbstractUser):
    """şifreleri kendisi otomatik olarak yeni hashe geçiriyon, yalnızca kullanıcının bir kere login olması yeterli """
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=40, blank=True, null=True)
    objects = UserObjects()

    class Meta:
        db_table = 'User'
        ordering = ["-id"]
        search_fields = ["id", "first_name", "last_name"]

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    @property
    def full_name_prop(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def verify(self, code):
        if not self.is_verified:
            if self.verification_code == code:
                self.update(is_verified=True)
        return self.is_verified


