# Generated by Django 4.1 on 2022-12-26 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Uploader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_ip', models.CharField(max_length=40)),
                ('cookie', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('upload_path', models.TextField()),
                ('identifier', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('delete_at', models.DateTimeField()),
                ('remaining_downloads', models.IntegerField(null=True)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uploader.uploader')),
            ],
        ),
    ]
