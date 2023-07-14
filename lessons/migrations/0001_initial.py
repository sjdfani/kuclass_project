# Generated by Django 3.2.18 on 2023-07-12 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('major', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('master_name', models.CharField(max_length=80, verbose_name='Master name')),
                ('unit', models.IntegerField(default=0, verbose_name='Unit')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='major.major', verbose_name='Major')),
            ],
        ),
    ]