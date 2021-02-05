from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        # based on doc
        # https://docs.djangoproject.com/en/2.2/topics/testing/tools/
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@domain.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@domain.com',
            password='password123',
            name="John Doe"
        )

    def test_user_listed(self):
        '''Test that users are lister on user page'''
        # check https://docs.djangoproject.com/en/3.1/ref/urlresolvers/#reverse
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        '''Test that the user edit page works'''
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/1
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        '''Test that the create user page works'''
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
