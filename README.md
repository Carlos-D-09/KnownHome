# KnownHome

Repositorio publico para el servidor del proyecto KnownHome

## Requisitos
- Tener instalada la versión de python 3.11.5 (No importa que no sea la principal del sistema)
- Contar con la herramienta virtualenv
- MySQL (SGBD por defecto para la creación y manipulacion de la base de datos)

## Instalación del proyecto (Windows)
 
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

## Instalación del proyecto (Linux)

### Preparación del entorno
Despues de clonar el repositorio, el primer paso para correr el proyecto es preparar el entorno donde se ejecutará, para ello abre en una terminal la carpeta "KnownHome" y ejecuta los siguiente comandos: 
```
virtualenv -p 3.11 venv
. venv/bin/activate
python -m pip install -r requirements.txt
```

Los comandos anteriores nos permitirán crear un entorno virtual con la versión de python que necesita el proyecto e instalar las dependencias necesarias para ejecutarlo.

### Configuración del archivo .env
El proyecto requiere de ciertas variables de entorno para funcionar, las cuales vienen ya escritas en una plantilla env.example. Para usarla copia y renombra el archivo .env.example a .env, y posteriormente ajustar los valores del archivo .env a los apropiados para nuestro equipo. A continuación se presenta un ejemplo del archivo .env:
```
SGBD="mysql" #By default the project works with mysql
DATABASE_HOST="localhost"
DATABASE_PORT="3306"
DATABASE_USER="test"
DATABASE="test"
DATABASE_PASSWORD="12345"

#Configuración aplicación
FLASK_APP='modular' #Don't change the name
APP_EMAIL = 'example@example.com'
APP_EMAIL_PASSWORD = 'password'
SECRET_KEY = 'secret_key'
MODEL = '/my_model.keras'
```
> [!NOTE]
> - APP_EMAIL y APP_EMAIL_PASSWORD son credenciales de aplicación para el envio de correos electrónicos mediante SMTP
> - Puedes consultar como generar una secret key [aquí](https://flask.palletsprojects.com/en/2.3.x/config/#:~:text=Default%3A%20None-,SECRET_KEY,-%C2%B6)
> - MODEL debe tener una ruta valida a un modelo keras compatible con tensorflow 2.14

### Corriendo la apliación por primera vez
El siguiente paso es crear la estructa de la base de datos necesaria para que el proyecto funcione, para ello es necesario ejecutar al menos una vez el proyecto, lo cual podemos hacer mediante cualquiera de los siguientes comandos:
```
flask run
flask run --debug
```

Ya que se ha corrido por primera vez la aplicación, ya seremos capaces de inicializar la base de datos, para ello utilizamos el siguiente comando: 
```
flask init-db
```
> [!IMPORTANT]
> Es necesario que la base de datos haya sido previamente creada, no importa si esta contiene algo o no, el script se encargara de vaciar la base de datos y volver a generar las tablas.  

Con fines de desarrollo, la aplicación cuenta con un método de poblamiento para la base de datos con registros de prueba, para hacer uso de ellos es necesario tener una base de datos en vacía y con la estructura de tablas generadas con el comando `init-db`. Para llevar a cabo este poblamiento utilice el siguiente comando: 
```
flask seed-db
```
