# Generated by Django 3.2.4 on 2021-07-13 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_jugement_lisible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='juridiction',
            name='type_juridiction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='search.typejuridiction'),
        ),
    ]
