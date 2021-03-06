# Generated by Django 3.0 on 2020-01-01 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0013_auto_20191231_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='posts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[(1, 'User'), (2, 'Moderator'), (3, 'Admin')], default=1, max_length=50),
        ),
    ]
