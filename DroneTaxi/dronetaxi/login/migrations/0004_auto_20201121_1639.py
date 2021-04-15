# Generated by Django 3.1.3 on 2020-11-21 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20201121_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['email'], 'verbose_name': 'Аккаунт пользователя', 'verbose_name_plural': 'Аккаунты пользователей'},
        ),
        migrations.AddField(
            model_name='user',
            name='user_role',
            field=models.CharField(choices=[('adm', 'Администратор'), ('clt', 'Клиент'), ('opr', 'Оператор')], default='clt', max_length=3, verbose_name='Роль пользователя'),
        ),
    ]
