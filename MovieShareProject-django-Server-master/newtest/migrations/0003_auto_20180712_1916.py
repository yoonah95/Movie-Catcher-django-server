# Generated by Django 2.0.5 on 2018-07-12 10:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('newtest', '0002_auto_20180712_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]