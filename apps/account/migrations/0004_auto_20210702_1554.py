# Generated by Django 3.2.4 on 2021-07-02 13:54

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_auto_20210701_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agent',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='agent',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='agent',
            name='id',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='user',
        ),
        migrations.AddField(
            model_name='agent',
            name='user_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user'),
            preserve_default=False,
        ),
    ]
