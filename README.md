# Servidor modular

Este el repositorio para trabajar el servidor que utilizaremos en el proyecto modular para la carreara de Ingenieria de Software.

**Requisitos**
- python >= 3.11.5
- flask >= 2.3.x
- pip >= 23.x
- MySQL (SGBD por defecto para la creación y manipulacion de la base de datos)

**Modulos de python** 
  - flask
  - flask-sqlalchemy
  - sqlalchemy-seeder
  - mysqlclient
  - flask_login
  - python-dotenv
  - flask-cors
  - tensorflow >= 2.10 <= 2.14
  - numpy
  - pillow

*Nota: Para trabajar en local mediante el entorno virtual, es necesario instalar los modulos mediante pip una vez inicializado el entorno virtual.

**Correr el projecto (local)**

**Windows (PowerShell)**

Despues de clonar el repositorio, entra en la carpeta "servidor-modular" y ejecuta los siguiente comandos: 
1. python -m venv venv
2. . venv/scripts/activate
3. pip install Flask flask-sqlachemy mysqlclient flask_login python-dotenv flask-cors sqlalchemy-seeder numpy pillow tensorflow==2.14

Copiamos y renombramos el archivo .env.example por .env, para posteriormente ajustar los valores del .env a los apropiados para nuestro equipo. 

El siguiente paso es correr la aplicación para ello podemos usar cualquiera de los dos comandos siguientes:
- flask run
- flask run --debug

Una vez que se ha corrido por primera vez la aplicación, ya seremos capaces de inicializar la base de datos, para ello utilizamos el siguiente comando: 
- flask init-db

Una vez inicializada la base de datos, podemos volver a ejecutar la aplicación y el servidor estara trabajando normal. Para verificar que la creación de las tablas se haya realizado de manera correcta, visualizala en MySQL. 

*Nota: Es necesario que la base de datos haya sido previamente creada, no importa si esta contiene algo o no, el script se encarga de vaciar la base de datos y volver a generar las tablas. 

Con fines de desarrollo, la aplicación cuenta con un método de poblamiento para la base de datos con registro de prueba, para hacer uso de ellos, es necesario tener una base de datos con la estructura de tablas generadas con el comando init-db. Para llevar a cabo este poblamiento utilice el siguiente comando: 
- flask seed-db

**Linux (local)**

Despues de clonar el repositorio, entra en la carpeta "servidor-modular" y ejecuta los siguiente comandos: 
1. python -m venv venv
2. . venv/bin/activate
3. pip install Flask flask-sqlachemy mysqlclient flask_login python-dotenv flask-cors qlalchemy-seeder numpy pillow tensorflow==2.14

Copiamos y renombramos el archivo .env.example por .env, para posteriormente ajustar los valores del .env a los apropiados para nuestro equipo. 

El siguiente paso es correr la aplicación para ello podemos usar cualquiera de los dos comandos siguientes:
- flask run
- flask run --debug

Ya que se ha corrido por primera vez la aplicación, ya seremos capaces de inicializar la base de datos, para ello utilizamos el siguiente comando: 
- flask init-db

Una vez que se ha corrido por primera vez la aplicación, ya seremos capaces de inicializar la base de datos, para ello utilizamos el siguiente comando: 

*Nota: Es necesario que la base de datos haya sido previamente creada, no importa si esta contiene algo o no, el script se encarga de vaciar la base de datos y volver a generar las tablas. 

Con fines de desarrollo, la aplicación cuenta con un método de poblamiento para la base de datos con registro de prueba, para hacer uso de ellos es necesario tener una base de datos en vacía y con la estructura de tablas generadas con el comando init-db. Para llevar a cabo este poblamiento utilice el siguiente comando: 
- flask seed-db
