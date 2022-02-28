from django.contrib.auth.models import Permission, User
from django.test import TestCase

from .forms import CountryForm, PersonForm
from .models import Country


class PermissionedFormTest(TestCase):
    def test_unbound_form_without_user(self):
        form = PersonForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        form_html = form.as_p()
        self.assertInHTML('<input type="text" name="first_name" required id="id_first_name">', form_html)
        self.assertInHTML('<input type="text" name="last_name" required id="id_last_name">', form_html)

    def test_bound_form_without_user(self):
        form = PersonForm({'first_name': 'David', 'last_name': 'Bowie'})
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['first_name'], 'David')
        self.assertEqual(form.cleaned_data['last_name'], 'Bowie')
        form_html = form.as_p()
        self.assertInHTML('<input type="text" name="first_name" value="David" required id="id_first_name">', form_html)
        self.assertInHTML('<input type="text" name="last_name" value="Bowie" required id="id_last_name">', form_html)

    def test_unbound_form_for_superuser(self):
        superuser = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        form = PersonForm(for_user=superuser)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        form_html = form.as_p()
        self.assertInHTML('<input type="text" name="first_name" required id="id_first_name">', form_html)
        self.assertInHTML('<input type="text" name="last_name" required id="id_last_name">', form_html)

    def test_bound_form_for_superuser(self):
        superuser = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        form = PersonForm({'first_name': 'David', 'last_name': 'Bowie'}, for_user=superuser)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['first_name'], 'David')
        self.assertEqual(form.cleaned_data['last_name'], 'Bowie')
        form_html = form.as_p()
        self.assertInHTML('<input type="text" name="first_name" value="David" required id="id_first_name">', form_html)
        self.assertInHTML('<input type="text" name="last_name" value="Bowie" required id="id_last_name">', form_html)

    def test_unbound_form_for_normal_user(self):
        bob = User.objects.create_user('bob', 'bob@example.com', 'password')
        form = PersonForm(for_user=bob)
        self.assertIn('first_name', form.fields)
        self.assertNotIn('last_name', form.fields)
        form_html = form.as_p()
        self.assertInHTML('<input type="text" name="first_name" required id="id_first_name">', form_html)
        self.assertInHTML('<input type="text" name="last_name" required id="id_last_name">', form_html, count=0)

    def test_bound_form_for_normal_user(self):
        bob = User.objects.create_user('bob', 'bob@example.com', 'password')
        form = PersonForm({'first_name': 'David', 'last_name': 'Bowie'}, for_user=bob)
        self.assertIn('first_name', form.fields)
        self.assertNotIn('last_name', form.fields)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['first_name'], 'David')
        self.assertNotIn('last_name', form.cleaned_data)
        form_html = form.as_p()
        self.assertInHTML('<input type="text" name="first_name" value="David" required id="id_first_name">', form_html)
        self.assertInHTML('<input type="text" name="last_name" value="Bowie" required id="id_last_name">', form_html, count=0)


class PermissionedModelFormTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Ukraine", description="A lovely country with a blue and yellow flag")
        self.edit_permission = Permission.objects.get(codename='change_country_description')

    def test_unbound_form_without_user(self):
        form = CountryForm(instance=self.country)
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        form_html = form.as_p()
        self.assertInHTML('<input type="text" name="name" maxlength="255" value="Ukraine" required id="id_name">', form_html)
        self.assertInHTML('<textarea name="description" cols="40" rows="10" id="id_description">A lovely country with a blue and yellow flag</textarea>', form_html)

    def test_bound_form_without_user(self):
        form = CountryForm({'name': 'France', 'description': 'A lovely country with baguettes'}, instance=self.country)
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'France')
        self.assertEqual(form.cleaned_data['description'], 'A lovely country with baguettes')
        form.save()
        self.assertEqual(self.country.name, 'France')
        self.assertEqual(self.country.description, 'A lovely country with baguettes')

    def test_unbound_form_for_superuser(self):
        superuser = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        form = CountryForm(instance=self.country, for_user=superuser)
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        form_html = form.as_p()
        self.assertInHTML('<input type="text" name="name" maxlength="255" value="Ukraine" required id="id_name">', form_html)
        self.assertInHTML('<textarea name="description" cols="40" rows="10" id="id_description">A lovely country with a blue and yellow flag</textarea>', form_html)

    def test_bound_form_for_superuser(self):
        superuser = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        form = CountryForm({'name': 'France', 'description': 'A lovely country with baguettes'}, instance=self.country, for_user=superuser)
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'France')
        self.assertEqual(form.cleaned_data['description'], 'A lovely country with baguettes')
        form.save()
        self.assertEqual(self.country.name, 'France')
        self.assertEqual(self.country.description, 'A lovely country with baguettes')

    def test_unbound_form_for_normal_user_with_permission(self):
        bill = User.objects.create_user('bill', 'bill@example.com', 'password')
        bill.user_permissions.add(self.edit_permission)
        form = CountryForm(instance=self.country, for_user=bill)
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        form_html = form.as_p()
        self.assertInHTML('<input type="text" name="name" maxlength="255" value="Ukraine" required id="id_name">', form_html)
        self.assertInHTML('<textarea name="description" cols="40" rows="10" id="id_description">A lovely country with a blue and yellow flag</textarea>', form_html)

    def test_bound_form_for_normal_user_with_permission(self):
        bill = User.objects.create_user('bill', 'bill@example.com', 'password')
        bill.user_permissions.add(self.edit_permission)
        form = CountryForm({'name': 'France', 'description': 'A lovely country with baguettes'}, instance=self.country, for_user=bill)
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'France')
        self.assertEqual(form.cleaned_data['description'], 'A lovely country with baguettes')
        form.save()
        self.assertEqual(self.country.name, 'France')
        self.assertEqual(self.country.description, 'A lovely country with baguettes')

    def test_unbound_form_for_normal_user_without_permission(self):
        bob = User.objects.create_user('bob', 'bob@example.com', 'password')
        form = CountryForm(instance=self.country, for_user=bob)
        self.assertIn('name', form.fields)
        self.assertNotIn('description', form.fields)
        form_html = form.as_p()
        self.assertInHTML('<input type="text" name="name" maxlength="255" value="Ukraine" required id="id_name">', form_html)
        self.assertInHTML('<textarea name="description" cols="40" rows="10" id="id_description">A lovely country with a blue and yellow flag</textarea>', form_html, count=0)

    def test_bound_form_for_normal_user_without_permission(self):
        bob = User.objects.create_user('bob', 'bob@example.com', 'password')
        form = CountryForm({'name': 'Sweden', 'description': 'A lovely country with flatpack furniture'}, instance=self.country, for_user=bob)
        self.assertIn('name', form.fields)
        self.assertNotIn('description', form.fields)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'Sweden')
        self.assertNotIn('description', form.cleaned_data)
        form.save()
        self.assertEqual(self.country.name, 'Sweden')
        self.assertEqual(self.country.description, 'A lovely country with a blue and yellow flag')
