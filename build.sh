# Construir imagenes de docker y contenedores
docker-compose up -d && \

# Make a symlink so static folder can pic-up npm dependencies
docker exec flask ln -s ../../node_modules/ app/static/

# Reiniciar contenedor para que las traducciones se apliquen
docker restart flask
