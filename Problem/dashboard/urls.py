from django.urls import path, include
from .views import AppViewSet, SubscriptionViewSet, PlanViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'apps', AppViewSet)
router.register(r'plans', PlanViewSet)
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]