# Generated by Django 3.0 on 2019-12-13 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20191211_0258'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='url',
            field=models.CharField(blank=True, default='no data', max_length=200),
        ),
    ]