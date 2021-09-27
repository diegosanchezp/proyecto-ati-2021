# Proyecto ATI Semestre 1-2021

## Requerimientos antes de levantar los contenedores
En la carpeta raiz existe una archivo `.env.example` haga una copia del mismo, renombre la copia a `.env` abra este archivo con su editor de texto y asignele un valor a la variable `SECRET_KEY`

Si tiene un distribucion`GNU/Linux` puede hacer la copia y el renombre con el siguiente comando

```sh
cp .env.example .env
```

## Trabajando con docker

Ejecute los siguientes comandos para construir y levantar los contenedores de docker, estos son pasos obligatorios

```sh
chmod +x build.sh && ./build.sh
```

## Dependencias de node (npm)

Si se hace un cambio a los archivos de código fuente ubicados en `static_src` hay que recompilarlos, para hacer esto constantemente ejecute los siguientes comandos dependiendo de que tipo de archivo

- Para recompilar CSS
```sh
docker exec flask npm run dev-css
```

## Logs de contenedores de flask, mongo y email_server

- Ver los logs de ambos contenedores

```sh
docker-compose logs --follow
```

## Servidor de emails

El servidor de emails es un programa de python que cuando mandas un email lo imprime en la terminal, no lo manda al destinatario, es decir, que si usted pone su email personal no le va a llegar un correo.


### Ver emails

Para ver los emails que se mandan a un destinatario, ejecutar

```
docker logs -f email_server
```

## Arquitectura o estructura del código

El proyecto se compone de los módulos `mural`, `chat`, `notificaciones`, y `usuarios`

Esto lo puede ver reflejado en el árbol de archivos del proyecto
```sh
proyecto-ati-2021
├── app
│   ├── chat
│   │   ├── __init__.py
│   │   └── vistas.py
│   ├── config.py
│   ├── __init__.py
│   ├── models
│   │   └── user.py
│   ├── mural
│   │   ├── __init__.py
│   │   └── vistas.py
│   ├── notificaciones
│   │   ├── __init__.py
│   │   └── vistas.py
│   ├── static
│   │   └── css
│   │       ├── raiz.css
│   │       └── raiz.css.map
│   ├── static_src
│   │   ├── css
│   │   │   └── raiz.scss
│   │   └── js
│   │       └── raiz.ts
│   ├── templates
│   │   ├── base.html
│   │   ├── chat
│   │   │   └── chat.html
│   │   ├── components
│   │   │   ├── mural
│   │   │   │   ├── comentario.html
│   │   │   │   └── publicacion.html
│   │   │   └── pagination.html
│   │   ├── mural
│   │   │   └── mural.html
│   │   ├── notificaciones
│   │   │   └── notificaciones.html
│   │   └── usuario
│   │       └── usuario.html
│   ├── test.py
│   ├── usuario
│   │   ├── __init__.py
│   │   └── vistas.py
│   └── utils.py
├── docker-compose.yml
├── docker-entrypoint.sh
├── Dockerfile
├── package.json
├── package-lock.json
├── README.md
├── requirements.txt
├── run.py
```

## Arquitectura para archivos CSS
Se utiliza el patron de arquitectura `7-1`. Para saber más del mismo, visite

https://sass-guidelin.es/es/#arquitectura

## Reglas de desarrollo

### En donde va la lógica de las vistas ?
Para crear vistas diríjase a la carpeta del modulo de interés y abra el archivo vistas.py

### Necesito separar código, puedo crear archivos adicionales ?
Si, cree los archivos adicionales que considere necesarios en la carpeta del módulo de interés

### Donde escribo el código html de las vistas ?
En la carpeta `templates`, la carpeta templates tiene sub-carpetas que corresponden a los módulos, ahí es donde pondrá el código html

### Donde escribo el código css y js de las vistas ?
En la carpeta `app/static_src/css` o `app/static_src/js` dependiendo del caso.

### Como creo una vista nueva
Cree una función nueva en el archivo `vistas.py` del módulo de interés y decorela con el blueprint definido

### Donde se definen las urls de las vistas ?
Se definen en `app/utils.py`

### Puedo cambiar el nombre de los archivos ?
Si puede cambiar los nombres de los archivos en la carpeta `app/template/` y `app/static_src/`

No cambie
- Los nombres de las carpetas principales que se muestran en la arquitectura, ya que se utilizan para la importación de módulos de python
- El nombre de los archivos `vistas.py`

### Como utilizo iconos de bootstrap
Para poner un icono de bootstrap en su html

1) Identifique primero el nombre icono que quiere utilizar, esto lo puede hacer rápidamente con el buscador de
https://icons.getbootstrap.com/

2) Añada una etiqueta img con el source y el nombre_icono
```html
<img src="{{ url_for('static', filename='node_modules/bootstrap-icons/icons/<nombre_icono>.svg') }}"
```

Como puede observar todos los iconos son archivos que se ubican en la carpeta node_modules/bootstrap-icons/icons y estos estan en formato svg, si el nombre del archivo difiere del que encontró en la página, inspeccione el contenido de la carpeta

## Traduciones ( i18n )

Las traducciones se realizan con [Flask-Babel](https://flask-babel.tkte.ch), el procedimiento es el siguiente
1) Marco un string como traducible en archivos *.py o *.html
2) Genero las traducciones para los strings marcados con el comando `pybabel`

### Realizar traducciones en archivos *.py

Importe y llame una de las siguientes funciones que marcan un string como traducible, dependiendo del caso, puede importar una o varias, no es necesario importarlas todas todas.

```py
from flask_babel import gettext, ngettext, _
```

Para mas información consulte la documentación de babel

https://flask-babel.tkte.ch/#using-translations

### Realizar traducciones en archivos *.html o templates

Las funciones que se importaron anteriormente también son accesibles desde los templates de `jinja2` sin importarlas ya que están en el contexto global de flask.

Por ejemplo para marcar un string traducible en html
```html
<!-- app/templates/components/sidebar.html -->

<!-- Marcamos el string "Ver todos mis amigos" como traducible -->
<a class="btn btn-primary" href="{{ url_for("usuario_blueprint.mis_amigos") }}">{{ _("Ver todos mis amigos") }}</a>
```

### Segundo paso: Generar las traducciones

Las traducciones se hacen en archivos de extensión *.po y se guardan en `app/translations`, actualmente se esta considerando un solo idioma para traducir, el inglés `en`.

1) Generar traducciones
```bash
### Extraer strings que se marcaron a un archivo donde se pondrán las traducciones
pybabel extract -F babel.cfg -k lazy_gettext,_l -o messages.pot .
# Actualizar traducciones con los nuevos strings marcados
pybabel update -i messages.pot -d app/translations
```

2) Abra el archivo `app/translations/en/LC_MESSAGES/messages.po` encuentre el string que quiere traducir y rellene el `msgstr ""`
```bash
### Compilar traducciones para que sean utilizables por babel
pybabel compile -d app/translations
```

**Importante** después de que compile las traducciones, tiene que reiniciar el contenedor de docker de flask o el servidor, si no hace esto, no vera las traducciones en la página web

```bash
### Reiniciar contenedor de flask
docker restart flask
```

## Pruebas unitarias de selenium

Las pruebas unitarias de selenium **solo se pueden correr dentro del contenedor del servico de flask**.

Debe de tener en cuenta las precondiciones que se listan en la [matriz de pruebas](https://docs.google.com/spreadsheets/d/1caXQq9I3zi7K1eNlq3zNJNa2p0VWPFOK/edit?usp=sharing&ouid=103607191941499792375&rtpof=true&sd=true)

```sh
# Entrar al contenedor que corre el servicio de flask
docker exec -it flask bash

# Correr todas las pruebas unitarias de selenium
python3 -m unittest discover -v -s app/tests/ -p "test_*.py"
```

Si desea ejecutar una sola prueba unitaria

```sh
python3 -m unittest app/tests/test_login.py
```
