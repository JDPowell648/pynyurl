import uuid
import uvicorn
import urllib.parse
from fastapi import FastAPI
from sqlalchemy import Connection, Engine, Text, create_engine, insert, text

app = FastAPI()

@app.get("/")
def read_root(): #Hello World!
    return {"Hello": "World"}


@app.get("/new/") #This will generate a shortened URL from a URL that a user delivers to it
def shortenURL(longURL: str):

    shortURL: str = uuid.uuid4().hex[0:6] #probably should do it better than this! placeholder
    longURL = urllib.parse.unquote(longURL) #maybe unneeded

    engine: Engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/pynyurl")
    conn: Connection = engine.connect()
    query: Text = text("INSERT INTO urls (longURL, shortURL) VALUES ('" + longURL +"'), ('"+shortURL+"');")
    conn.execute(query)
    conn.commit()

    return {"shortURL": shortURL, "longURL": longURL}

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

