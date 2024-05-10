# PYnyURL
## What is PYnyURL?
This is PYnyURL, a short and sweet project to play around with python and other associated tools such as FastAPI, SQLAlchemy, and Docker.

## How Do I Build This Project?
To build this project, run `docker compose up --build` in your terminal of choice. This will create the associated images for the postgres database and the api.
You can hit the API at `host/new?longurl=MY/URL/HERE` to create a shortened URL of 7 characters.
Then, you are able to use this shortened URL at `host/use/MYSHORTURL`

## Other Setup
Be sure to create a .env file with the following variables to run the project:
POSTGRES_DB_NAME, POSTGRES_DB_USER, POSTGRES_DB_PASS, POSTGRES_DB_HOST, POSTGRES_DB_PORT, APP_HOST, APP_PORT