from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Plan, App, Subscription
from .serializers import PlanSerializer, AppSerializer, SubscriptionSerializer

class AppViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_app(self):
        data = {'name': 'App', 'description': 'Description'}
        response = self.client.post('/dashboard/apps/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(App.objects.count(), 1)
        self.assertEqual(Subscription.objects.count(), 1)


    def test_get_apps(self):
        App.objects.create(owner=self.user, name='Facebook', description='Description of Facebook')
        App.objects.create(owner=self.user, name='Linkedin', description='Description of linkedin')
        response = self.client.get('/dashboard/apps/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class PlanViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)


    def test_get_plans(self):
        Plan.objects.create(name='Plan 1', price=10.0)
        Plan.objects.create(name='Plan 2', price=20.0)
        response = self.client.get('/dashboard/plans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

class SubscriptionViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.plan1 = Plan.objects.create(name='Plan 1', price=10.0)
        self.plan2 = Plan.objects.create(name='Plan 2', price=20.0)
        self.app = App.objects.create(owner=self.user, name='Test App', description='Test Description')
        self.subscription = Subscription.objects.create(app=self.app, plan=self.plan1, active=True)

    def test_update_subscription_plan(self):
        data = {'app':self.app.id, 'plan': self.plan2.id}
        response = self.client.patch(f'/dashboard/subscriptions/{self.subscription.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['plan']['id'], self.plan2.id)

    def test_deactivate_subscription(self):
        response = self.client.delete(f'/dashboard/subscriptions/{self.subscription.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.get(id=self.subscription.id).active)