# Generated by Django 3.0.6 on 2020-06-12 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Carrito",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "estatus",
                    models.CharField(default="OPEN", help_text="Estado", max_length=50),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CarritoProducto",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cantidad", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Categoria",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fc", models.DateTimeField(auto_now_add=True)),
                ("fm", models.DateTimeField(auto_now=True)),
                (
                    "Nombre",
                    models.CharField(
                        help_text="Nombre de la categoria", max_length=50, unique=True
                    ),
                ),
            ],
            options={"verbose_name": "Categoria", "verbose_name_plural": "Categorias",},
        ),
        migrations.CreateModel(
            name="TipoProducto",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fc", models.DateTimeField(auto_now_add=True)),
                ("fm", models.DateTimeField(auto_now=True)),
                (
                    "Nombre",
                    models.CharField(help_text="Nombre de la categoria", max_length=50),
                ),
                (
                    "Descripcion",
                    models.CharField(
                        help_text="Descripcion de la categoria",
                        max_length=100,
                        unique=True,
                    ),
                ),
                ("Um", models.CharField(help_text="Unidad de Medida", max_length=50)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="producto.Categoria",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Tipos de Productos",},
        ),
        migrations.CreateModel(
            name="Producto",
            fields=[
                ("fc", models.DateTimeField(auto_now_add=True)),
                ("fm", models.DateTimeField(auto_now=True)),
                (
                    "Nombre",
                    models.CharField(help_text="Nombre de producto", max_length=40),
                ),
                (
                    "codigo",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("precio", models.FloatField(default=0)),
                (
                    "descripcion",
                    models.CharField(
                        default="descripcion ",
                        help_text="Descripcion de productos",
                        max_length=100,
                    ),
                ),
                (
                    "Marca",
                    models.CharField(
                        default="Marca", help_text="Marca del producto", max_length=100
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        blank=True,
                        help_text="Color del producto",
                        max_length=20,
                        null=True,
                    ),
                ),
                ("Stock", models.IntegerField()),
                ("imagen", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "Categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="producto.Categoria",
                    ),
                ),
                (
                    "TipoProducto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="producto.TipoProducto",
                    ),
                ),
            ],
            options={"verbose_name": "Producto", "verbose_name_plural": "Productos",},
        ),
    ]