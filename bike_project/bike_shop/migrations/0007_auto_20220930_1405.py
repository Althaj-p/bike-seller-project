# Generated by Django 3.2.13 on 2022-09-30 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bike_shop', '0006_bikes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='bikes',
            name='brakes',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='engine',
            field=models.FloatField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='fuel',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='fuel_tank',
            field=models.FloatField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='mileage',
            field=models.FloatField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='power',
            field=models.FloatField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='torque',
            field=models.FloatField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='weight',
            field=models.FloatField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='bikes',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bike_shop.type'),
        ),
    ]
