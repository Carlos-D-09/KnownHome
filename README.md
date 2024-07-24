# KnownHome

This public repository is for the KnownHome project server. The project has the following objectives: 
- Use a pre-trained neural network model to classify objects in images.
- Implement API consumption for a mobile application. 
- Implement a web page to manage mobile application transactions.

> [!NOTE]
> - The list of objects that can be classified with the neural network is written into the file `/modular/__init__.py`
> - You can consult the code to create the neuronal network [here](https://github.com/Carlos-D-09/object-recognition)

## Requirements
- Has Python 3.11.5 installed (It doesn't matter if It's not the main system version) 
- virtualenv tool 
- MySQL (Default DBMS to create and manipulate the database) 

## Project installation

### Preparing environment (Windows - Powershell)
After cloning the repository, open a terminal as an administrator in the "KnownHome" directory  and execute the following commands: 
```
virtualenv -p 3.11 venv
. venv/scripts/activate
python3 -m pip install -r requirements.txt 
```
These commands create a virtual environment with the correct Python version needed for the project and install the necessary dependencies.

### Preparing environment (Linux)
Open a terminal in the "KnownHome" directory and execute the following commands: 
```
virtualenv -p 3.11 venv
. venv/bin/activate
python -m pip install -r requirements.txt
```

> [!NOTE]
> The command `virtualenv - p 3.11` venv searches the specified Python version into the default executable path. If your Python version executable is installed on a different path, you must specify the path in the command. To achieve this, you can use the next command: `virtualenv --python /path/to/your/python venv`

### Setting the .env file
The project requires certain environment variables to work, which are written into a template .env.example. To use it, copy and rename the file .env.example to .env,  and then adjust the values according to your equipment. Below is an example of a .env file: 
```
SGBD="mysql" #By default the project works with mysql
DATABASE_HOST="localhost"
DATABASE_PORT="3306"
DATABASE_USER="test"
DATABASE="test"
DATABASE_PASSWORD="12345"

#Application configuration
FLASK_APP='modular' #Don't change the name
APP_EMAIL = 'example@example.com'
APP_EMAIL_PASSWORD = 'password'
SECRET_KEY = 'secret_key'
MODEL = '/my_model.keras'
```
> [!NOTE]
> - APP_EMAIL and APP_EMAIL_PASSWORD are application credentials to send emails through the SMTP protocol
> - You can learn how to generate a secret key  [here](https://flask.palletsprojects.com/en/2.3.x/config/#:~:text=Default%3A%20None-,SECRET_KEY,-%C2%B6)
> - MODEL must have a valid path to a keras model compatible with TensorFlow 2.14

### Running the application for the first time
The next step is to create the database structure needed for the project. To achieve this, it's essential to execute at least once and then immediately end the execution. To run the project, you can use either of these commands: 
```
flask run
flask run --debug
```
> [!NOTE]
> - The virtualenv must be active
> - To finish the run process, use the key combination ctrl+c

Once the application has been executed one time, you will be able to create the database structure with the following command: 
```
flask init-db
```
> [!IMPORTANT]
> The database must have been created previously, it doesn´t matter if it is empty or not. The script will empty the database and generate the tables.

For development purposes, the application has a seeding method for the database, which contains test records. To use this method, the database must be empty, and the tables generated with the command init-db. To seed the database, use the following command: 
```
flask seed-db
```
