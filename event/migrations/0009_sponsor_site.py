# Generated by Django 3.0.8 on 2020-08-13 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='site',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='сайт'),
        ),
    ]
