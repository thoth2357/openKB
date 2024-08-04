from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

@receiver(post_migrate)
def create_default_settings(sender, **kwargs):
    call_command('init_settings')
