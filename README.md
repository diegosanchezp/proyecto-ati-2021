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
docker compose up --build -d
```

Compilar codigo fuente sass

```sh
docker exec flask npm run build
```
## Dependencias de node (npm)

Si se hace un cambio a los archivos de código fuente ubicados en `static_src` hay que recompilarlos, para hacer esto constantemente ejecute los siguientes comandos dependiendo de que tipo de archivo

- Para recompilar CSS
```sh
docker exec flask npm run dev-css
```

## Logs de contenedores de flask y mongo

- Ver los logs de ambos contenedores
```sh
docker-compose logs --follow
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
