# Grupo 8

Este es el repositorio del *Grupo 8*, cuyos integrantes son:
* Benjamin Soto   - 202204516-7
* Pamela Sánchez  - 202273538-4
* Mariano Varas   - 202273611-9
* Felipe Vallejos - 202173653-0
* **Tutor**: Diego Debarca 

## Wiki
Puede acceder a la Wiki mediante el siguiente [enlace](https://gitlab.com/analisis-y-dise-o-de-software/Vigifia/-/wikis/home)

## Videos

* [Video presentacion del cliente](https://www.youtube.com/watch?v=abJau21SDIk)
* [Video final](https://www.youtube.com/watch?v=tYey6C8v0t0)

## Instrucciones para ejecutar proyecto con Docker

* En primera instancia, es necesario tener Docker instalado en su SO (más detalles en este [enlace](https://docs.docker.com/engine/install/))


* Después, migrar los cambios hechos al proyecto ejecutando:

{

    docker exec -it django_webapp bash

    python manage.py makemigrations

    python manage.py migrate

}

* Luego, estando en el directorio del proyecto (Vigifia), abrir una terminal y ejecutar:

{

    docker-compose build # para construir el proyecto y sus requerimientos

}

y

{

    docker-compose up # para levantar el contenedor del proyecto
    
}

* Finalmente, entrar a localhost:8000/ para ver el contenido del proyecto

