# Generated by Django 3.1.3 on 2020-11-23 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20201123_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operator', to='login.user'),
        ),
    ]
