# Generated by Django 3.2.13 on 2022-09-25 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike_shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('slug', models.SlugField(null=True)),
                ('logo', models.FileField(null=True, upload_to='')),
            ],
        ),
    ]
