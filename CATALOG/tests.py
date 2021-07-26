from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class UserAccountTests(TestCase):

    def test_create_superuser(self):
        
        group = Group.objects.create(name='school-admin-group')

        db = get_user_model()
        super_user = db.objects.create_superuser(
            email='test-superuser@gmail.com',
            user_name='Test-Superuser',
            password='Password',
            )
        self.assertEqual(super_user.email, 'test-superuser@gmail.com')
        self.assertEqual(super_user.user_name, 'Test-Superuser')
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), 'Test-Superuser')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            email='test-superuser1@gmail.com',
            user_name='Test-Superuser1',
            password='Password1',
            is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            email='test-superuser1@gmail.com',
            user_name='Test-Superuser1',
            password='Password1',
            is_staff=False)

    def test_create_user(self):
        
        group = Group.objects.create(name='school-admin-group')
        group.save()

        db = get_user_model()
        user = db.objects.create_user(
            email='test-user@gmail.com',
            user_name='Test-User',
            type=2,
            password='Password',
            )
        self.assertEqual(user.email, 'test-user@gmail.com')
        self.assertEqual(user.user_name, 'Test-User')
        self.assertEqual(user.type, 2)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(str(user), 'Test-User')

    def test_create_school_admin(self):
        
        content_type = ContentType.objects.get(app_label='CATALOG', model='student')

        permission1 = Permission.objects.create(codename='can_view_student', name='Can view student', content_type=content_type)
        permission2 = Permission.objects.create(codename='can_add_student', name='Can add student', content_type=content_type)
        permission3 = Permission.objects.create(codename='can_change_student', name='Can change student', content_type=content_type)
        permission4 = Permission.objects.create(codename='can_delete_student', name='Can delete student', content_type=content_type)

        group = Group.objects.create(name='school-admin-group')
        group.permissions.add(permission1, permission2, permission3, permission4)
        group.save()

        db = get_user_model()
        user = db.objects.create_user(
            email='test-school-admin@gmail.com',
            user_name='Test-School-Admin',
            type=2,
            password='Password',
            )

        self.assertEqual(user.email, 'test-school-admin@gmail.com')
        self.assertEqual(user.user_name, 'Test-School-Admin')
        self.assertEqual(user.type, 2)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(str(user), 'Test-School-Admin')

        self.assertTrue(user.has_perm('CATALOG.can_add_student'))
        self.assertTrue(user.has_perm('CATALOG.can_view_student'))
        self.assertTrue(user.has_perm('CATALOG.can_change_student'))
        self.assertTrue(user.has_perm('CATALOG.can_delete_student'))
        self.assertFalse(user.has_perm('CATALOG.can_delete_school'))
