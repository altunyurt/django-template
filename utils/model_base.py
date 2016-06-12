# ~*~ coding:utf-8 ~*~

from .helpers import reverse_lazy, slugify, one_or_none
from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet, Q
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage
import re
import os
import ujson

import logging
logger = logging.getLogger(__name__)

models.options.DEFAULT_NAMES += ("search_fields", "slug_field")
tag_re = re.compile("<[^>]*>|[\r\n]|[\s\t]+")


class SearchableQuerySet(QuerySet):
    def search(self, word):
        search_fields = getattr(self.model._meta, "search_fields", [])
        if not search_fields:
            raise Exception("SearchableQuerySet search_fields meta alanını gerektirir")
        return self.filter(reduce(lambda x, y: x | y,
                                  [Q(**{"%s__icontains" % field_name: word}) for field_name in search_fields]))


class QuerySetManager(models.Manager):
    def get_query_set(self):
        """
            Eger bir class icinde queryset tanimi yapilmamissa ilk yuklemede patliyor.
            Asagidaki kontrol bunu engelliyor
        """
        if hasattr(self.model, 'QuerySet'):
            return self.model.QuerySet(self.model)

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

    def first(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs and qs[0] or None


class _Model(models.Model):
    """
        UNCached abstract Model class for enabling simple addition of chainable
        manager methods to models.
    """
    objects = QuerySetManager()

    class Meta:
        abstract = True

    def to_dict(self):
        d = model_to_dict(self, fields=[field.name for field in self._meta.fields])
        d.update(model_to_dict(self, fields=[field.name for field in self._meta.many_to_many]))
        return d

    def to_json(self):
        return ujson.dumps(self.to_dict())

    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save()
        return self

    @property
    def slug(self):
        slug_field = getattr(self._meta, "slug_field")
        if not slug_field:
            return ""
        return slugify(getattr(self, slug_field))


_UNSAVED_FILEFIELD = 'unsaved_filefield'

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.unlink(os.path.join(settings.MEDIA_ROOT, name))
        return name

# henüz instance yokken id ile kaydedememe problemini gidermek için
def skip_saving_file(sender, instance, **kwargs):
    if not instance.pk and not hasattr(instance, _UNSAVED_FILEFIELD):
        field = "file" if (instance.__class__.__name__ == "Ad") else "image"
        setattr(instance, _UNSAVED_FILEFIELD, getattr(instance, field))
        setattr(instance, field, None)


def save_file(sender, instance, created, **kwargs):
    if created and hasattr(instance, _UNSAVED_FILEFIELD):
        field = (instance.__class__.__name__ == "Ad") and "file" or "image"
        setattr(instance, field, getattr(instance, _UNSAVED_FILEFIELD))
        instance.save()
        instance.__dict__.pop(_UNSAVED_FILEFIELD)
