# Generated by Django 2.1.7 on 2020-08-20 01:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jugador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.PositiveSmallIntegerField()),
                ('fecha', models.DateField(auto_now=True)),
                ('calificador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calificacion_calificador', to='jugador.Jugador')),
            ],
        ),
        migrations.CreateModel(
            name='Confirmacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_equipo', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='JugadorEnEquipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now=True)),
                ('id_equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_equipo', to='emparejamiento.Equipo')),
                ('id_jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_jugador', to='jugador.Jugador')),
            ],
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('estado', models.CharField(default='por jugar', max_length=10)),
                ('id_equipo1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipo_equipo1', to='emparejamiento.Equipo')),
                ('id_equipo2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipo_equipo2', to='emparejamiento.Equipo')),
            ],
        ),
        migrations.AddField(
            model_name='jugadorenequipo',
            name='id_partido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_partido', to='emparejamiento.Partido'),
        ),
        migrations.AddField(
            model_name='confirmacion',
            name='id_jugador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_confirmador', to='emparejamiento.JugadorEnEquipo'),
        ),
        migrations.AddField(
            model_name='calificacion',
            name='id_partido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calificacion_partido', to='emparejamiento.Partido'),
        ),
        migrations.AddField(
            model_name='calificacion',
            name='jugador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calificacion_jugador', to='jugador.Jugador'),
        ),
    ]
