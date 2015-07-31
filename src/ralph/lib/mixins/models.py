# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def get_admin_url(obj, action):
    content_type = ContentType.objects.get_for_model(obj.__class__)
    return reverse(
        "admin:{}_{}_{}".format(
            content_type.app_label, content_type.model, action
        ),
        args=(obj.id,)
    )


def get_field_by_relation_path(model, field_path):
    """
    Returns field for `model` referenced by `field_path`.

    E.g. calling:
        get_field_by_relation_path(BackOfficeAsset, 'model__manufacturer__name')
    returns:
        <django.db.models.fields.CharField: name>
    This is achieved by dynamically executing such code:
        self.model.\
        _meta.get_field('model').related_model.\
        _meta.get_field('manufacturer').related_model.\
        _meta.get_field('name')
    """
    def get_related_model(model, field_name):
        related_model = model._meta.get_field(field_name).related_model
        return related_model

    hops = field_path.split('__')
    relation_hops, dst_field = hops[:-1], hops[-1]
    for field_name in relation_hops:
        model = get_related_model(model, field_name)
    found_field = model._meta.get_field(dst_field)
    return found_field


class NamedMixin(models.Model):
    """Describes an abstract model with a unique ``name`` field."""
    name = models.CharField(_('name'), max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    class NonUnique(models.Model):
        """Describes an abstract model with a non-unique ``name`` field."""
        name = models.CharField(verbose_name=_("name"), max_length=75)

        class Meta:
            abstract = True

        def __str__(self):
            return self.name


class TimeStampMixin(models.Model):
    created = models.DateTimeField(
        verbose_name=_('date created'),
        auto_now=True,
    )
    modified = models.DateTimeField(
        verbose_name=_('last modified'),
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-modified', '-created',)

    class Permissions:
        blacklist = set(['created', 'modified'])


class LastSeenMixin(models.Model):
    last_seen = models.DateTimeField(
        verbose_name=_('last seen'),
        auto_now_add=True,
    )

    class Meta:
        abstract = True

    def save(self, update_last_seen=False, *args, **kwargs):
        if update_last_seen:
            self.last_seen = timezone.now()
        super(LastSeenMixin, self).save(*args, **kwargs)


class AdminAbsoluteUrlMixin(object):
    def get_absolute_url(self):
        return reverse(
            'admin:{}_{}_change'.format(
                self._meta.app_label, self._meta.model_name
            ), args=(self.pk,)
        )
