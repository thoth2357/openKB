from django.core.management.base import BaseCommand
from kb.models import WebsiteSettings, ArticleSettings, DisplaySettings,StyleSettings

class Command(BaseCommand):
    help = 'Initialize settings models with default values'

    def handle(self, *args, **kwargs):
        if not WebsiteSettings.objects.exists():
            WebsiteSettings.objects.create()
            self.stdout.write(self.style.SUCCESS('WebsiteSettings initialized with default values.'))

        if not ArticleSettings.objects.exists():
            ArticleSettings.objects.create()
            self.stdout.write(self.style.SUCCESS('ArticleSettings initialized with default values.'))

        if not DisplaySettings.objects.exists():
            DisplaySettings.objects.create()
            self.stdout.write(self.style.SUCCESS('DisplaySettings initialized with default values.'))

        if not StyleSettings.objects.exists():
            StyleSettings.objects.create()
            self.stdout.write(self.style.SUCCESS('StyleSetting initialized with default values.'))