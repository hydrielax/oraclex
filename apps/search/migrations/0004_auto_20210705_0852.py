# Generated by Django 3.2.4 on 2021-07-05 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_jugement_nom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugement',
            name='gain',
            field=models.FloatField(blank=True, help_text='Somme gagnée lors du procès (négative si perdu)', null=True, verbose_name='Somme gangée'),
        ),
        migrations.AlterField(
            model_name='jugement',
            name='juridiction',
            field=models.ForeignKey(blank=True, help_text='Cour ou Conseil du jugement', null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.typejuridiction', verbose_name='Juridiction'),
        ),
    ]
