from django.test import TestCase
from django.urls import reverse

from .models import User


class RoleAccessTests(TestCase):

    def setUp(self):
        self.donor = User.objects.create_user(
            username='d', password='pass12345', role='DONOR'
        )
        self.ngo = User.objects.create_user(
            username='n', password='pass12345', role='NGO'
        )
        self.admin = User.objects.create_user(
            username='a', password='pass12345', role='ADMIN'
        )

    def test_login_required(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_admin_dashboard_blocked_for_donor(self):
        self.client.login(username='d', password='pass12345')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_allowed_for_admin(self):
        self.client.login(username='a', password='pass12345')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_ngo_dashboard_blocked_for_donor(self):
        self.client.login(username='d', password='pass12345')
        response = self.client.get(reverse('ngo_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_api_forbidden_for_donor(self):
        self.client.login(username='d', password='pass12345')
        response = self.client.get(reverse('api_available_donations'))
        self.assertEqual(response.status_code, 403)

    def test_api_allowed_for_ngo(self):
        self.client.login(username='n', password='pass12345')
        response = self.client.get(reverse('api_available_donations'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)
