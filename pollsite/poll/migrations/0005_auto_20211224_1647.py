# Generated by Django 2.1.7 on 2021-12-24 11:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0004_auto_20211224_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='meeting_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Published'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Title of Meeting'),
        ),
    ]
