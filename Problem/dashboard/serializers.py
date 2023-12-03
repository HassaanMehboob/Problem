from rest_framework import serializers
from .models import App, Plan, Subscription
from django.contrib.auth.models import User

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    class Meta:
        model = Subscription
        fields = ['id', 'app', 'plan', 'active']

class AppSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = App
        fields = ['id', 'owner', 'name', 'description', 'subscriptions'] 