# Generated by Django 3.0.5 on 2020-07-11 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0003_auto_20200710_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(max_length=18, primary_key=True, serialize=False),
        ),
    ]