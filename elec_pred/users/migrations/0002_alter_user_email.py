# Generated by Django 5.1.1 on 2024-10-01 19:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(
                blank=True,
                max_length=254,
                null=True,
                verbose_name='email address',
            ),
        ),
    ]
