# Generated by Django 2.0.5 on 2018-05-17 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MicrowaveStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('On', models.BooleanField(default=False)),
                ('TTL', models.PositiveSmallIntegerField()),
                ('Power', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
