# Generated by Django 4.0 on 2022-01-11 10:03

from django.db import migrations
import markdownfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0015_meeting_desc_rendered_alter_meeting_desc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='desc_rendered',
            field=markdownfield.models.RenderedMarkdownField(),
        ),
    ]
