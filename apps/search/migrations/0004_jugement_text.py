# Generated by Django 3.2.4 on 2021-07-13 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_alter_juridiction_nom'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugement',
            name='text',
            field=models.TextField(null=True, verbose_name='Texte'),
        ),
    ]
