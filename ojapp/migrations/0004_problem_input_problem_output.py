# Generated by Django 4.0.5 on 2022-07-05 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ojapp', '0003_solution_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='input',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AddField(
            model_name='problem',
            name='output',
            field=models.CharField(default=1, max_length=255),
        ),
    ]
