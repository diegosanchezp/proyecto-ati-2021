# Construir imagenes de docker y contenedores
docker-compose up --build -d && \

# Compilar codigo fuente sass
docker exec flask npm run build && \

# Make a symlink so static folder can pic-up npm dependencies
docker exec flask ln -s ../../node_modules/ app/static/

# Compilar traducciones
docker exec flask pybabel compile -d app/translations && \

# Reiniciar contenedor para que las traducciones se apliquen
docker restart flask
