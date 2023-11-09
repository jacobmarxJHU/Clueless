# Single-database configuration for Flask.

I was having trouble with the alembic directory when initializing the database, and I think it may have been because
the directory name was "alembic" instead of the expected "migrations." So I just initialized again and have been using
the migrations directory.

## Running migrations
When changes are made to the models file, use the flask-migrate package to send those changes to the database. 
Navigate to the flask server directory and perform the following: 

```bash
flask db migrate
flask db upgrade
```
The migrate command will commit changes, and the upgrade command will push those changes.
