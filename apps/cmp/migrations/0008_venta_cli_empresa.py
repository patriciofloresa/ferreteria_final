# Generated by Django 3.0.8 on 2020-07-04 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmp', '0007_venta_tipo_documento'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='cli_empresa',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Empresa'),
        ),
    ]