# Generated by Django 3.2.18 on 2023-07-12 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='state',
            field=models.CharField(choices=[('done', 'Done'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending', max_length=10, verbose_name='State'),
        ),
    ]
