from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0004_comentario'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramaRadio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_programa', models.CharField(max_length=200)),
                ('apresentador', models.CharField(blank=True, max_length=200)),
                ('horario_inicio', models.TimeField()),
                ('horario_fim', models.TimeField()),
            ],
            options={
                'verbose_name': 'Programa de Rádio',
                'verbose_name_plural': 'Programação da Rádio',
                'ordering': ['horario_inicio'],
            },
        ),
    ]
