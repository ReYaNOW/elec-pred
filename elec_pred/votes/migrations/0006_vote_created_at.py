# Generated by Django 5.1.1 on 2024-10-10 00:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('votes', '0005_alter_choice_options_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2024, 10, 10, 0, 9, 0, 902274, tzinfo=datetime.timezone.utc
                ),
            ),
            preserve_default=False,
        ),
    ]
