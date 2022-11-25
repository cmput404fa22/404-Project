# Generated by Django 4.1.2 on 2022-11-24 03:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_alter_post_received'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='is_remote_node',
        ),
        migrations.CreateModel(
            name='RemoteNode',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('base_url', models.TextField()),
                ('team', models.IntegerField()),
                ('registered', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]