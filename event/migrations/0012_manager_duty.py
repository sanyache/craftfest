# Generated by Django 3.0.8 on 2020-08-17 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_manager_middle_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='duty',
            field=models.TextField(blank=True, null=True, verbose_name='відповідальний за'),
        ),
    ]
