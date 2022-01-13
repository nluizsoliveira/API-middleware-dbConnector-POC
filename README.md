# amdocs-onboarding-project
A frontend/backend website using API/middleware/dbConnector pattern implementation for a simple library system (Python, Mysql, JS, HTML, CSS)

![print of the application](/print.png)

## **Features implemented/used:**
- `.env` file for managing passwords, virtualenv and requirements.txt for managing packages
- `db_connector.py`: defines a Class for interacting with mysql database
- `middleware.py`: defines a Class for instantiating a `DbConnector`, implementing business logic, preparing parameters for contextualized queries for the application and calling its db_connector to execute the queries
- `api.py`: defines uses Flask to define an API that instantiates Midleware, populates the db if the table `books` does not exists, exposes a port and defines specific routes according to business logic to be called from frontend, executing Middlewares functions when necessary and handeling/responsing JSONs.
- `front.html`: defines the structure of the visual browser page used by user. Links front.js and style.css.
- `style.css`: defines the styling (colours, identation, spacing, shadows) of the application
- `front.js`: request data to the port served by api.py. Waits for the response in JSON format and mounts the page contents using HTMLElements (Dom manipulation). Each button is binded with a function that calls the api and trigger deleting the content of the page and mounting it again, according the business logic.



## Project Requirements
- Python 3
- virtualenv
- mysql

## How to run: Setting up backend
0. **Create a virtual environment and install python dependencies**
If you are using a unix-like system, commands are:

```shell
virtualnv -p $(which python3) myenv
source myenv
pip install -r requirements.txt
```

You will see a (myenv) befofe your bash commands now. You can leave the enviroment later using

```shell
deactivate
```
1. **Create a Login, Password and Database in Mysql if you don't have one yet**
2. **Store the login, password and database credentials in a .env file**
create a `.env` file. Save your credentials in the following format:
```shell
export DATABASE_USER="youruser"
export DATABASE_PASSWORD="yourpassword"
export DATABASE_NAME="yourdatabasename"
```
3. **Save the credentials on your eviroment variables**
If you are on unix-like system, the command is:
```shell
source .env
```
to unset a variable later, you can use
```shell
unset variable
```
4. **Start the server**
run: 
```shell
python3 api.py
```

The backend will start to run on a port (**probably 5000**). That number is important, it's the number frontend wil request to. 

## How to run: Setting up frontend
0. **Check if front.js port is the same as api.py is running**
1. **open front.html in a browser**
3. Have fun :)