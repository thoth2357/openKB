
from kb.models import StyleSettings, WebsiteSettings


def website_settings(request):
    # Retrieve the settings; you may handle the case when there are no settings.
    website_settings = WebsiteSettings.objects.first()
    style_settings = StyleSettings.objects.first()

    # Return a dictionary of the settings to be added to the template context
    return {
        'websettings': website_settings,
        'style_settings': style_settings,
    }
