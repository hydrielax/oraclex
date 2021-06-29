# Generated by Django 3.2.4 on 2021-06-29 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupeMotCle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True, verbose_name='Groupe')),
            ],
            options={
                'verbose_name': 'Groupe de mots-clés',
                'verbose_name_plural': 'Groupes de mots-clés',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Responsable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=50, verbose_name='Prénom')),
                ('nom', models.CharField(max_length=50, verbose_name='Nom')),
                ('telephone', models.CharField(max_length=17, verbose_name='Téléphone')),
                ('mail', models.EmailField(max_length=254, verbose_name='Email')),
                ('en_charge', models.BooleanField(help_text='Vrai si le responsable est actuellement en charge.')),
            ],
            options={
                'ordering': ['nom', 'prenom'],
            },
        ),
        migrations.CreateModel(
            name='TypeJuridiction',
            fields=[
                ('cle', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='Abbréviation')),
                ('nom', models.CharField(max_length=40, verbose_name='Type')),
                ('niveau', models.IntegerField(help_text='Niveau de hiérarchie (1=première instance, 2 ensuite, etc...)', verbose_name='Niveau')),
            ],
            options={
                'verbose_name': 'Type de Juridiction',
                'verbose_name_plural': 'Types de Juridiction',
                'ordering': ['niveau', 'nom'],
            },
        ),
        migrations.CreateModel(
            name='MotCle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True, verbose_name='Mot-Clé')),
                ('variante1', models.CharField(blank=True, max_length=50, null=True, verbose_name='Variante 1')),
                ('variante2', models.CharField(blank=True, max_length=50, null=True, verbose_name='Variante 2')),
                ('variante3', models.CharField(blank=True, max_length=50, null=True, verbose_name='Variante 3')),
                ('groupe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.groupemotcle')),
            ],
            options={
                'verbose_name': 'Mot-clé',
                'verbose_name_plural': 'Mots-clés',
                'ordering': ['groupe', 'nom'],
            },
        ),
        migrations.CreateModel(
            name='Juridiction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=70, null=True)),
                ('ville', models.CharField(blank=True, max_length=40, null=True)),
                ('rattachement', models.ForeignKey(blank=True, help_text="Cour d'Appel de rattachement dans le cas d'un Conseil des Prud'Hommes", limit_choices_to={'type_juridiction': 'CA'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.juridiction', verbose_name='Cour de rattachement')),
                ('type_juridiction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.typejuridiction')),
            ],
            options={
                'ordering': ['type_juridiction', 'ville'],
            },
        ),
        migrations.CreateModel(
            name='Jugement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='jugements', verbose_name='Fichier')),
                ('lisible', models.BooleanField(help_text="Vrai si le fichier est lisible par l'ordinateur.", verbose_name='Lisible')),
                ('decision', models.CharField(blank=True, choices=[('F', 'Favorable'), ('D', 'Défavorable'), ('M', 'Mixte')], help_text='Décision de justice', max_length=1, null=True, verbose_name='Décision')),
                ('date_jugement', models.DateField(blank=True, help_text='Date du jugement', null=True, verbose_name='Date du jugement')),
                ('date_import', models.DateTimeField(auto_now_add=True, verbose_name="Date d'import du jugement")),
                ('gain', models.FloatField(blank=True, help_text='Somme gagnée lors du procès (négative si perdu)', null=True)),
                ('juridiction', models.ForeignKey(blank=True, help_text='Cour ou Conseil du jugement', null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.typejuridiction')),
                ('mots_cle', models.ManyToManyField(blank=True, help_text='Mots-clé présents dans le Jugement', null=True, to='search.MotCle', verbose_name='Mot-Clé')),
            ],
            options={
                'ordering': ['-date_jugement'],
            },
        ),
    ]