<p align="center">
<a href="https://pypi.org/project/django-permissionedforms/">
    <img src="https://badge.fury.io/py/django-permissionedforms.svg" alt="Package version">
</a>
<a href="https://opensource.org/licenses/BSD-3-Clause">
    <img src="https://img.shields.io/badge/license-BSD-blue.svg"/>
</a>
</p>

django-permissionedforms
========================

`django-permissionedforms` is an extension to Django's forms framework, allowing you to define forms where certain fields are shown or omitted according to the user's permissions.

* [Changelog](https://github.com/wagtail/django-permissionedforms/blob/main/CHANGELOG.md)


Requirements
------------

* Python 3.7 or higher
* Django 3.2 or higher


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


Integrating with other base form classes
----------------------------------------

You may wish to integrate the permission handling from `django-permissionedforms` into some other base form class, such as `ClusterForm` from the [django-modelcluster](https://github.com/wagtail/django-modelcluster) package. If that base form class is a straightforward subclass of `django.forms.Form` or `django.forms.ModelForm`, then using multiple inheritance to additionally inherit from `PermissionedForm` or `PermissionedModelForm` should work:

```python
from fancyforms import FancyForm  # made up for example purposes
from permissionedforms import PermissionedForm

class FancyPermissionedForm(PermissionedForm, FancyForm):
    pass
```

However, this will fail if the base form class implements its own metaclass. In this case, you will need to define a new metaclass inheriting from both the existing one and `permissionedforms.PermissionedFormMetaclass`:

```python
from fancyforms import FancyForm
from permissionedforms import PermissionedForm, PermissionedFormMetaclass


FancyFormMetaclass = type(FancyForm)


class FancyPermissionedFormMetaclass(PermissionedFormMetaclass, FancyFormMetaclass):
    pass


class FancyPermissionedForm(PermissionedForm, FancyForm, metaclass=FancyPermissionedFormMetaclass):
    pass
```

This could still fail if the base form class incorporates a custom Options class to allow it to accept its own `class Meta` options. If so, it will be necessary to define a new Options class, again using multiple inheritance to subclass both the existing Options class and `permissionedforms.PermissionedFormOptionsMixin`, and then set this as `options_class` on the metaclass. The following recipe will work for `ClusterForm`:

```python
from modelcluster.forms import ClusterForm, ClusterFormMetaclass, ClusterFormOptions
from permissionedforms import PermissionedForm, PermissionedFormMetaclass, PermissionedFormOptionsMixin


class PermissionedClusterFormOptions(PermissionedFormOptionsMixin, ClusterFormOptions):
    pass


class PermissionedClusterFormMetaclass(PermissionedFormMetaclass, ClusterFormMetaclass):
    options_class = PermissionedClusterFormOptions


class PermissionedClusterForm(PermissionedForm, ClusterForm, metaclass=PermissionedClusterFormMetaclass):
    pass
```


Support
-------

For support, please use [GitHub Discussions](https://github.com/wagtail/django-permissionedforms/discussions) or the [Wagtail Slack workspace](https://github.com/wagtail/wagtail/wiki/Slack).


Contributing
------------

Install this package in development mode:

```shell
git clone https://github.com/wagtail/django-permissionedforms.git
cd django-permissionedforms
pip install -e .[testing]
```

To run the test suite locally:

```shell
make test
```

To generate a test coverage report:

```shell
make coverage
```

To check the code style of all files:

```shell
make lint
```

To fix any errors that can be automatically fixed:

```shell
make format
```

Security
--------
If you have found a security issue with this project please email us at [security@wagtail.org](mailto:security@wagtail.org) so we can work together to find and patch the issue. We appreciate responsible disclosure with any security related issues, so please contact us first before creating a Github issue.

If you want to send an encrypted email (optional), the public key ID for security@wagtail.org is `0xbed227b4daf93ff9`, and this public key is available from most commonly-used keyservers.


Acknowledgements
----------------

`django-permissionedforms` was developed as part of [Wagtail](https://wagtail.org/)'s next-generation page editor, sponsored by Google.
