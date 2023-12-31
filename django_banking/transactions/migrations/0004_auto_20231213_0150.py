# Generated by Django 3.1.8 on 2023-12-13 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transaction_tipo_ativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ativo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Nome do ativo', max_length=255)),
                ('tipo', models.PositiveSmallIntegerField(choices=[(6, 'Fundos'), (7, 'Ações'), (8, 'Títulos Públicos'), (9, 'Criptomoedas')])),
                ('descricao', models.TextField(blank=True, help_text='Descrição detalhada do ativo', null=True)),
                ('preco_atual', models.DecimalField(blank=True, decimal_places=2, help_text='Preço atual do ativo', max_digits=10, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tipo_ativo',
            field=models.PositiveSmallIntegerField(choices=[(6, 'Fundos'), (7, 'Ações'), (8, 'Títulos Públicos'), (9, 'Criptomoedas')]),
        ),
    ]
