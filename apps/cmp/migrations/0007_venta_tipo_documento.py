# Generated by Django 3.0.8 on 2020-07-04 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmp', '0006_auto_20200703_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='tipo_documento',
            field=models.CharField(choices=[('BOLETA', 'Boleta'), ('FACTURA', 'Factura')], default='BOLETA', max_length=15, null=True, verbose_name='Tipo documento'),
        ),
    ]