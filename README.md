# Grupo 8

Este es el repositorio del *Grupo 14*, cuyos integrantes son:
* Cristóbal Espinoza Latorre - 202273565-1
* Benjamin Soto              - 202204516-7
* Renato Roggia              - 202204594-9
* Mariano Varas              - 202273611-9
* **Tutor**: Eduardo Pino 


## Info

Este es el mismo proyecto que se presentó para el ramo INF236 y se seguirá trabajando para INF225.

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

