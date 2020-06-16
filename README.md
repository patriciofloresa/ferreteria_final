# Ferreteria Django

Este proyecto es para la Tesis de la universidad...

para generar el MER con la liberia de django-extension hacer lo siguiente:

```sh

--instalar los paquetes que se encuentra en nuestro requirements.txt

-- Añadir en el settings.py la siguiente app:

INSTALLED_APPS = [  
    ...
    'django_extensions',
]

```

Por ultimo correr el siguiente comando:

```sh
python3 manage.py graph_models --pygraphviz -a -g -o MER_ALL_MODELS.png
```

Para crear el gráfico se debe iniciar el siguiente comando al interior del proyecto:

```sh

-- Genera un grafico del app seleccionada (api)
$ python manage.py graph_models api -o APP_MODELS.png

-- Genera grafico de todos los modelos incluyendo los que vienen por defecto de Django
$ python3 manage.py graph_models --pygraphviz -a -g -o MER_ALL_MODELS.png

```
## Recomendaciones
Descargar e instalar ubuntu 18.04 LTS
Instalar el certificado SSL local

ssl localse recomienda en vez de usar vim pasarse a nano
https://kifarunix.com/how-to-create-self-signed-ssl-certificate-with-mkcert-on-ubuntu-18-04/

Para acceder a la base local usar las siguientes credenciales:

Acceso 1:

- **usuario:** admin
- **contraseña:** 123

Acceso 2:

- **usuario:**jaime
- **contraseña:** 123

Acceso 3
- **usuario:** admin2
- **contraseña:** 123


Para ejecutar el proyecto con el certificado SSL escribir el siguiente comando

```sh

sudo python3 manage.py runsslserver --certificate /home/buho/example.com+4.pem --key /home/buho/example.com+4-key.pem

```
