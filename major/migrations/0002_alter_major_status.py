# Generated by Django 3.2.18 on 2023-07-14 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('major', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='major',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Status'),
        ),
    ]