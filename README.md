# Proyecto ATI Semestre 1-2021

## Trabajando con docker

Ejecute los siguientes comandos para construir y levantar los contenedores de docker
```sh
docker compose --build -d
```

## Dependencias de node (npm)

Si se hace un cambio a los archivos de código fuente ubicados en `static_src` hay que recompilarlos, para hacer esto constantemente ejecute los siguientes comandos dependiendo de que tipo de arhico

- Para recompilar CSS
```sh
docker exec flask npm run dev-css
```

## Logs de contenedores de flask y mongo

- Ver los logs de ambos contenedores
```sh
docker-compose logs --follow
```
