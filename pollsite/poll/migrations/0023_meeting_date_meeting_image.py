# Generated by Django 4.0 on 2022-01-12 10:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0022_question_first_correct_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of meeting'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Image for your meeting'),
        ),
    ]
