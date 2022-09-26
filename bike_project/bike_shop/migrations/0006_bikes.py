# Generated by Django 3.2.13 on 2022-09-25 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bike_shop', '0005_alter_company_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='bikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('image', models.FileField(upload_to='')),
                ('slug', models.SlugField(max_length=250)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('desc', models.TextField(max_length=500)),
                ('available', models.BooleanField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bike_shop.company')),
            ],
        ),
    ]
