django-permissionedforms
========================

`django-permissionedforms` is an extension to Django's forms framework, allowing you to define forms where certain fields are shown or omitted according to the user's permissions.


Installation
------------

Run: `pip install django-permissionedforms`


Usage
-----

To add permission rules to a basic Django form, subclass `permissionedforms.PermissionedForm` in place of `django.forms.Form` and add an inner `Meta` class:

```python
from permissionedforms import PermissionedForm

class PersonForm(PermissionedForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        field_permissions = {
            'last_name': 'myapp.change_last_name'
        }
```

`field_permissions` is a dict, mapping field names to permission codenames. For each field listed, that field will only be included in the final form if the user has the specified permission, as defined by the `user.has_perm()` method. See Django's documentation on [custom permissions](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#custom-permissions) and [programmatically creating permissions](https://docs.djangoproject.com/en/4.0/topics/auth/default/#programmatically-creating-permissions) for details on how to set permissions up; alternatively, if you want to set a field as only available to superusers, you can use any arbitrary string (such as `'superuser'`) as the codename, since `has_perm` always returns True for them.

Then, when instantiating the form, pass the keyword argument `for_user`:

```python
form = PersonForm(for_user=request.user)
```

This will result in a form where the `last_name` field is only present if the logged-in user has the `change_last_name` permission.

The keyword argument `for_user` is optional, and if not passed, the form will behave as an ordinary form with all named fields available.

For a ModelForm, the procedure is the same, except that you should inherit from `permissionedforms.PermissionedModelForm` instead. `field_permissions` is added alongside the existing `Meta` options:

```python
from permissionedforms import PermissionedModelForm

class CountryForm(PermissionedModelForm):
    class Meta:
        model = Country
        fields = ['name', 'description']
        field_permissions = {
            'description': 'tests.change_country_description'
        }

form = CountryForm(instance=country, for_user=request.user)
```
