# Generated by Django 3.1.8 on 2023-12-08 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20231207_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='tipo_ativo',
            field=models.PositiveSmallIntegerField(choices=[(6, 'Fundos'), (7, 'Ações'), (8, 'Títulos Públicos')], default=1),
            preserve_default=False,
        ),
    ]
