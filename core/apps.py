from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        username = "saurabh"
        password = "Admin@123"   # deploy ke baad CHANGE karna
        email = "admin@example.com"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
