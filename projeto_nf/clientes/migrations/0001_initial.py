# Generated by Django 5.1.4 on 2024-12-06 06:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logradouro', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=10)),
                ('bairro', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=2)),
                ('cep', models.CharField(max_length=8)),
                ('pais', models.CharField(max_length=50)),
                ('telefone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('tipo_documento', models.CharField(choices=[('CPF', 'CPF'), ('CNPJ', 'CNPJ')], max_length=4)),
                ('documento', models.CharField(max_length=14, unique=True)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.endereco')),
            ],
        ),
    ]