# Generated by Django 5.0.6 on 2024-07-04 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0005_registro_rut_alter_mascota_subtipo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='subtipo',
            field=models.CharField(choices=[('Otro', 'Otro'), ('Gato', [('Volador', 'Volador'), ('Nian', 'Nian')]), ('PERRO', [('Chico', 'Chico'), ('Grande', 'Grande'), ('Verde', 'Verde')]), ('Reptil', [('Lagarto', 'Lagarto'), ('Anaconda', 'Anaconda')])], default='Otro', max_length=20),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='tipo',
            field=models.CharField(choices=[('REPTIL', 'Reptil'), ('GATO', 'Gato'), ('OTRO', 'Otro'), ('PERRO', 'Perro')], max_length=15),
        ),
        migrations.AlterField(
            model_name='persona',
            name='sexo',
            field=models.CharField(choices=[('M', 'MASCULINO'), ('O', 'OTRO'), ('F', 'FEMENINO')], max_length=1),
        ),
        migrations.AlterField(
            model_name='producto',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]