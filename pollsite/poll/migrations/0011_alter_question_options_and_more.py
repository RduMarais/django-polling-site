# Generated by Django 4.0 on 2022-01-06 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0010_alter_question_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={},
        ),
        migrations.AlterOrderWithRespectTo(
            name='question',
            order_with_respect_to='meeting',
        ),
    ]
