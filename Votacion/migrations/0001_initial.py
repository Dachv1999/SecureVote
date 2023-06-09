# Generated by Django 4.2.1 on 2023-06-11 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Cuenta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PadronElectoral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant_votos', models.IntegerField(blank=True, null=True)),
                ('cant_vblanco', models.IntegerField(blank=True, null=True)),
                ('cant_vpositivo', models.IntegerField(blank=True, null=True)),
                ('cant_vnullo', models.IntegerField(blank=True, null=True)),
                ('total_votos', models.IntegerField(blank=True, null=True)),
                ('estado_result', models.CharField(choices=[('G', 'Ganador'), ('P', 'Perdedor'), ('E', 'Empatador')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ci_candidato', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Votacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_votacion', models.CharField(choices=[('N', 'Normal'), ('M', 'MayoriaAbsoluta')], default='N', max_length=1)),
                ('inicio_votacion', models.DateTimeField(blank=True, null=True)),
                ('fin_votacion', models.DateTimeField(blank=True, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('padron_electoral', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Votacion.padronelectoral')),
                ('partido1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partido1', to='Cuenta.partidoelectoral')),
                ('partido2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partido2', to='Cuenta.partidoelectoral')),
                ('partido3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partido3', to='Cuenta.partidoelectoral')),
                ('partido4', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partido4', to='Cuenta.partidoelectoral')),
            ],
        ),
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashvoto', models.CharField(blank=True, max_length=100, null=True)),
                ('tipo_voto', models.CharField(choices=[('P', 'Positivo'), ('A', 'Abstencion'), ('B', 'Blanco'), ('N', 'Nulo')], default='A', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ci_candidato', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidato', to=settings.AUTH_USER_MODEL)),
                ('ci_votante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votante', to=settings.AUTH_USER_MODEL)),
                ('id_votacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Votacion.votacion')),
            ],
        ),
        migrations.CreateModel(
            name='Voto_extended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voto_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Votacion.voto')),
            ],
        ),
        migrations.CreateModel(
            name='Votacion_extended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votacion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Votacion.votacion')),
            ],
        ),
        migrations.CreateModel(
            name='Resultado_extended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Votacion.resultado')),
            ],
        ),
        migrations.AddField(
            model_name='resultado',
            name='id_votacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Votacion.votacion'),
        ),
        migrations.CreateModel(
            name='PadronElectoralUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ci_usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_padron', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Votacion.padronelectoral')),
            ],
        ),
    ]
