# Discord_Bot_Template
A template for creating discord bots that run in python attached to a database. 

1. Start by creating an .env file in the same file path as the template .py file.
.env should look like

{

  API_TOKEN=""
  
  DB_DRIVER=""
  
  DB_SERVER=""
  
  DB_DATABASE=""
  
  USER_ID=""
  
  USER_SECRET="" 
  
}

2. Connect a database using this .env, if you do not want one attached to the bot, the functions that try to access it will not run if there is no connection.
3. There are some basic functions in the bottom #TODO, from there you can extrapolate and build on them.
4. Create a virtual environment to run the code in and install dependencies.

Do the following to run your bot:

$ py -m pip install --user virtualenv

$ py -m venv env

$ .\env\Scripts\activate

$ pip install -r requirements.txt

$ python bot_template.py

