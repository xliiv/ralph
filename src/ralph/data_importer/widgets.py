# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from django.contrib.contenttypes.models import ContentType
from import_export import widgets
import six

from ralph.assets.models.assets import ServiceEnvironment
from ralph.data_center.models.physical import DataCenterAsset
from ralph.back_office.models import BackOfficeAsset
from ralph.data_importer.models import ImportedObjects


logger = logging.getLogger(__name__)


class ImportedForeignKeyWidget(widgets.ForeignKeyWidget):

    """Widget for ForeignKey fields for which can not define unique."""

    def clean(self, value):
        result = None
        if value:
            content_type = ContentType.objects.get_for_model(self.model)
            imported_obj = ImportedObjects.objects.filter(
                content_type=content_type,
                old_object_pk=six.text_type(value)
            ).first()
            if imported_obj:
                result = self.model.objects.filter(
                    pk=int(imported_obj.object_pk)
                ).first()
            else:
                logger.warning(
                    "Record with pk {pk} not found for model {model}".format(
                        pk=imported_obj.object_pk,
                        model=self.model._meta.model_name
                    )
                )
        return result


class AssetServiceEnvWidget(widgets.ForeignKeyWidget):

    """Widget for AssetServiceEnv Foreign Key field.

    CSV field format Service.name|Environment.name
    """

    def clean(self, value):
        try:
            value = value.split("|")  # service, enviroment
            value = ServiceEnvironment.objects.get(
                service__name=value[0],
                environment__name=value[1]
            )
        except ServiceEnvironment.DoesNotExist:
            value = None
        return value

    def render(self, value):
        if value is None:
            return ""
        return "{}|{}".format(
            value.service.name,
            value.environment.name
        )


class BaseObjectWidget(widgets.ForeignKeyWidget):

    """Widget for BaseObject Foreign Key field.

    CSV field format: DataCenterAsset.sn or BackOfficeAsset.sn
    """

    def clean(self, value):
        asset = DataCenterAsset.objects.filter(sn=value).first()
        if not asset:
            asset = BackOfficeAsset.objects.filter(sn=value).first()
        if asset:
            return asset.baseobject_ptr
        return None

    def render(self, value):
        if value is None:
            return ""
        return value.id