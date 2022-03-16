from django import forms
from modelcluster.forms import ClusterForm, ClusterFormMetaclass, ClusterFormOptions

from permissionedforms import (
    PermissionedForm,
    PermissionedFormMetaclass,
    PermissionedFormOptionsMixin,
    PermissionedModelForm,
)

from .models import Country, Page


class PersonForm(PermissionedForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        field_permissions = {"last_name": "tests.change_last_name"}


class CountryForm(PermissionedModelForm):
    class Meta:
        model = Country
        fields = ["name", "description"]
        field_permissions = {"description": "tests.change_country_description"}


class PermissionedClusterFormOptions(PermissionedFormOptionsMixin, ClusterFormOptions):
    pass


class PermissionedClusterFormMetaclass(PermissionedFormMetaclass, ClusterFormMetaclass):
    options_class = PermissionedClusterFormOptions


class PermissionedClusterForm(
    PermissionedForm, ClusterForm, metaclass=PermissionedClusterFormMetaclass
):
    pass


class PageForm(PermissionedClusterForm):
    class Meta:
        model = Page
        fields = ["title", "body"]
        formsets = ["tags"]
        field_permissions = {"title": "tests.change_page_title"}
