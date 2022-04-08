#  Ninth Week Assignment.

# Logic Diagram of the project.
![Diagram](https://gitlab.com/t7501/fifth-week-assignment/-/blob/feature/django/models/img/Fifth%20Week%20Assignement%20UML.drawio.png)

# Instruction to run the app.

- You have to specify the environment variables (see .env-example).
- There are some details to consider when specifying those variables:
    - The environment variable "APP_STATE" (Local / Deploy) define if the
        Fast-API app uses the local database or specified URL database on
        heroku.
    
# Heroku app credential (pre-created-accounts) for testing JWT.
- Account with administrator permission. <br />
Email: admin@filmrentalsystem.com <br />
Password: admin12345678 

- Account with employee permission. <br />
Email: employee@filmrentalsystem.com <br />
Password: employee12345678 

Also, If you wish you can create your accounts using the following link.<br />

- Register your account. <br />
link: https://week10-film-rental-system.herokuapp.com/graphql

Look for the mutation "createUser"

# Heroku URLs for generate JWT token.
Note: This is using "Bearer" as the JWT prefix. 

link: https://week10-film-rental-system.herokuapp.com/graphql

Search for token mutation, and then put the username (email) and password of the 
user you want to use. 

Note: For almost all the mutations you have to pass the token as parameter.

# Heroku URl for API documentation. 
link: https://week10-film-rental-system.herokuapp.com/docs/

Note: Here you can use /api/poster/upload/{film_id} endpoint to upload poster 
images to S3.

# Commands to seed ten records by table.
Note: It would be a good idea to run the commands in the same order that
appears down to avoid errors for nonexistent data dependency.

- python command.py accountsgen --user_type (-a argument to create as admins or
-e argument to create as employees).
- python command.py categoriesgen
- python command.py filmsgen
- python command.py seasonsgen
- python command.py chaptersgen
- python command.py rolesgen
- python command.py personsgen
- python command.py clientsgen
- python command.py filmspersonsrolesgen
- python command.py rentsgen

# Heroku URL API apps (users, categories, films, seasons, chapters, persons, roles, films-persons-roles, clients and rents).
link: https://week10-film-rental-system.herokuapp.com/graphql


# Note about Phone number format in clients App.
The app receive phone number of the following format: "XXX-XXXX-XXXX" 
where X = number 

# Note about Date format.
Year-mouth-day example 2020-03-24