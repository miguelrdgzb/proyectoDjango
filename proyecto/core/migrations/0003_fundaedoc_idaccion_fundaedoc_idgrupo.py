# Generated by Django 4.1 on 2022-08-22 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_fundaedoc'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundaedoc',
            name='idAccion',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='fundaedoc',
            name='idGrupo',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
