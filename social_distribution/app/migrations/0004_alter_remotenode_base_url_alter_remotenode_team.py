# Generated by Django 4.1.2 on 2022-11-24 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_author_is_remote_node_remotenode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remotenode',
            name='base_url',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='remotenode',
            name='team',
            field=models.IntegerField(unique=True),
        ),
    ]
