# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from ralph.admin import RalphAdmin, register
from ralph.admin.fields import MultilineField, MultivalueFormMixin
from ralph.back_office.models import BackOfficeAsset, Warehouse
from ralph.back_office.views import (
    BackOfficeAssetComponents,
    BackOfficeAssetLicence,
    BackOfficeAssetSoftware
)
from ralph.data_importer import resources
from ralph.lib.permissions.admin import PermissionAdminMixin


class BackOfficeAssetForm(MultivalueFormMixin, forms.ModelForm):

    class Meta:
        model = BackOfficeAsset
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.id:
            self.fields['sn'] = MultilineField('sn')
            self.fields['barcode'] = MultilineField('barcode')
            self.multivalue_fields = ['sn', 'barcode']
            self.one_of_mulitvalue_required = ['sn', 'barcode']


@register(BackOfficeAsset)
class BackOfficeAssetAdmin(
    PermissionAdminMixin,
    RalphAdmin
):

    """Back Office Asset admin class."""

    change_views = [
        BackOfficeAssetComponents,
        BackOfficeAssetSoftware,
        BackOfficeAssetLicence,
    ]
    list_display = [
        'status', 'barcode', 'purchase_order', 'model', 'user', 'warehouse',
        'sn', 'hostname', 'invoice_date', 'invoice_no'
    ]
    search_fields = ['barcode', 'sn', 'hostname', 'invoice_no', 'order_no']
    list_filter = ['status']
    date_hierarchy = 'created'
    list_select_related = ['model', 'user', 'warehouse', 'model__manufacturer']
    raw_id_fields = ['model', 'user', 'owner', 'service_env']
    resource_class = resources.BackOfficeAssetResource
    form = BackOfficeAssetForm

    fieldsets = (
        (_('Basic info'), {
            'fields': (
                'hostname', 'model', 'barcode', 'sn', 'niw', 'status',
                'warehouse', 'location', 'loan_end_date', 'service_env',
                'remarks'
            )
        }),
        (_('User Info'), {
            'fields': (
                'user', 'owner'
            )
        }),
        (_('Financial Info'), {
            'fields': (
                'order_no', 'purchase_order', 'invoice_date', 'invoice_no',
                'task_url', 'price', 'depreciation_rate',
                'depreciation_end_date', 'force_depreciation', 'provider',

            )
        }),
    )


@register(Warehouse)
class WarehouseAdmin(RalphAdmin):

    search_fields = ['name']
