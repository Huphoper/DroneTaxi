# Generated by Django 3.1.3 on 2020-11-24 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20201123_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='production_year',
            field=models.IntegerField(default=2020, max_length=4),
        ),
    ]
