# Grupo 14

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



## Cómo levantar el proyecto con Docker

### 1. Requisitos previos
Antes de comenzar, asegúrate de tener Docker y Docker Compose instalados en tu sistema:

- **Instalar Docker**: [Guía oficial](https://docs.docker.com/engine/install/)
- **Instalar Docker Compose**: Ya viene incluido en Docker Desktop (para Mac y Windows).

---

### 2. Ubicación del proyecto
Abre una terminal y ubícate en el directorio del proyecto, donde se encuentran los archivos:

```bash
cd ruta/al/proyecto
```

---

### 3. Construir los contenedores
Ejecuta el siguiente comando para construir las imágenes del proyecto:

```bash
docker-compose build
```

Esto creará dos servicios:

- `web`: la aplicación Django.
- `db`: una base de datos PostgreSQL configurada con:
  - Usuario: `equipo`
  - Contraseña: `equipo123`
  - Base de datos: `isw`

---

### 4. Levantar los contenedores
Una vez construidos, levanta los contenedores con:

```bash
docker-compose up
```

La aplicación quedará disponible en `http://localhost:8000/`.

---

### 5. Aplicar migraciones
Con los contenedores corriendo, abre una terminal aparte y entra al contenedor de Django:

```bash
docker exec -it django_webapp bash
```

Y luego corre:

```bash
python manage.py makemigrations
python manage.py migrate
```

Esto aplicará las migraciones necesarias para que la base de datos quede operativa.

---

### 6. Acceder a la app
Abre tu navegador y ve a:

```
http://localhost:8000/
```

Ahí deberías ver la app funcionando correctamente.

