# Generated by Django 4.2.1 on 2023-06-12 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Votacion', '0002_alter_resultado_cant_vblanco_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='votacion',
            name='nombre',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
    ]