from django.db import migrations


def create_admin(apps, schema_editor):
    User = apps.get_model("auth", "User")

    username = "saurabh"
    password = "Admin@123"
    email = "admin@example.com"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0001_initial"),  # agar number alag ho to wahi likhna
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]

