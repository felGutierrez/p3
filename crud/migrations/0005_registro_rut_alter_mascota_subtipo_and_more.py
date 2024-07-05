# Generated by Django 5.0.6 on 2024-07-04 00:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0004_alter_mascota_subtipo_alter_mascota_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='rut',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='subtipo',
            field=models.CharField(choices=[('PERRO', [('Chico', 'Chico'), ('Grande', 'Grande'), ('Verde', 'Verde')]), ('Gato', [('Volador', 'Volador'), ('Nian', 'Nian')]), ('Otro', 'Otro'), ('Reptil', [('Lagarto', 'Lagarto'), ('Anaconda', 'Anaconda')])], default='Otro', max_length=20),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='tipo',
            field=models.CharField(choices=[('PERRO', 'Perro'), ('OTRO', 'Otro'), ('GATO', 'Gato'), ('REPTIL', 'Reptil')], max_length=15),
        ),
        migrations.AlterField(
            model_name='user',
            name='postal',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999999)]),
        ),
    ]