# Generated by Django 3.1.3 on 2020-11-21 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drone',
            options={'verbose_name': 'Дрон', 'verbose_name_plural': 'Дроны'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
    ]
