# Generated by Django 3.1.3 on 2020-11-28 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20201124_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='drone',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='login.drone'),
        ),
    ]