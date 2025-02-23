# Generated by Django 5.0.6 on 2024-06-26 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='subtipo',
            field=models.CharField(choices=[('Otro', 'Otro'), ('Reptil', [('Lagarto', 'Lagarto'), ('Anaconda', 'Anaconda')]), ('Gato', [('Volador', 'Volador'), ('Nian', 'Nian')]), ('PERRO', [('Chico', 'Chico'), ('Grande', 'Grande'), ('Verde', 'Verde')])], default='Otro', max_length=20),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='tipo',
            field=models.CharField(choices=[('GATO', 'Gato'), ('PERRO', 'Perro'), ('OTRO', 'Otro'), ('REPTIL', 'Reptil')], max_length=15),
        ),
        migrations.AlterField(
            model_name='persona',
            name='sexo',
            field=models.CharField(choices=[('F', 'FEMENINO'), ('M', 'MASCULINO'), ('O', 'OTRO')], max_length=1),
        ),
        migrations.AlterField(
            model_name='registro',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
