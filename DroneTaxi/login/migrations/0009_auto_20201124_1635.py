# Generated by Django 3.1.3 on 2020-11-24 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20201124_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='production_year',
            field=models.IntegerField(default=2020),
        ),
    ]
