# Generated by Django 4.0.2 on 2022-02-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads_scraper_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomRequirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(max_length=80)),
                ('hourly_rate', models.IntegerField()),
                ('budget', models.IntegerField()),
            ],
        ),
    ]
