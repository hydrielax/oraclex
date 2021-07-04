# Generated by Django 3.2.4 on 2021-07-02 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0004_auto_20210702_1554'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agent',
            options={},
        ),
        migrations.AlterModelManagers(
            name='agent',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='agent',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='agent',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]