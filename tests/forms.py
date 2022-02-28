from django import forms
from permissionedforms import PermissionedForm, PermissionedModelForm

from .models import Country


class PersonForm(PermissionedForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        field_permissions = {
            'last_name': 'tests.change_last_name'
        }


class CountryForm(PermissionedModelForm):
    class Meta:
        model = Country
        fields = ['name', 'description']
        field_permissions = {
            'description': 'tests.change_country_description'
        }
