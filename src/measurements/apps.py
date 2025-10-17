from django.apps import AppConfig


class MeasurementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'measurements'

    def ready(self):
        # Auto create user groups
        # Import here to avoid crash due to app registry not ready
        from django.contrib.auth.models import Group
        for group_name in ['Director', 'Manager', 'Engineer', 'EngineerAssistant']:
            Group.objects.get_or_create(name=group_name)
