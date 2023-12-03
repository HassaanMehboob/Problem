from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Plan

@receiver(post_migrate)
def create_initial_plans(sender, **kwargs):
    if sender.name == 'dashboard':
        Plan.objects.get_or_create(name='Free', price=0)
        Plan.objects.get_or_create(name='Standard', price=10)
        Plan.objects.get_or_create(name='Pro', price=25)