# Generated by Django 3.2.5 on 2021-07-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_url', models.URLField(verbose_name='Type Url Here')),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
