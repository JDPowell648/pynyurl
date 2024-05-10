from typing import Any
import uuid
import uvicorn
import urllib.parse
import os
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import Column, Connection, Engine, Integer, MetaData, Row, Sequence, Table, Text, Tuple, create_engine, insert, select, text

POSTGRES_DB_NAME=os.environ.get("POSTGRES_DB_NAME")
POSTGRES_DB_USER=os.environ.get("POSTGRES_DB_USER")
POSTGRES_DB_PASS=os.environ.get("POSTGRES_DB_PASS")
POSTGRES_DB_HOST=os.environ.get("POSTGRES_DB_HOST")
POSTGRES_DB_PORT=os.environ.get("POSTGRES_DB_PORT")
APP_HOST=os.environ.get("APP_HOST")
APP_PORT=os.environ.get("APP_PORT")

app = FastAPI()
metadata: MetaData = MetaData()
urls = Table(
        'urls',
        metadata,
        Column("shorturl", Text, nullable=False, primary_key=True),
        Column("longurl", Text, nullable=False),
        Column("interactions", Integer),
    )

@app.get("/new/") 
async def shortenURL(longurl: str):
    #This will generate a shortened URL from a URL that a user delivers to it
    #Pretty sure this should be a PUT or POST
    #Add success/fails

    longurl = urllib.parse.unquote(longurl) #maybe unneeded

    engine: Engine = create_engine("postgresql+psycopg2://%s:%s@%s:%s/%s" % (POSTGRES_DB_USER, POSTGRES_DB_PASS, POSTGRES_DB_HOST, POSTGRES_DB_PORT, POSTGRES_DB_NAME))
    conn: Connection = engine.connect()
    shorturl: str = ''
    res: int = -1
    while(res != 0):
        shorturl = uuid.uuid4().hex[0:7] #probably should do it better than this! placeholder
        query: Text = text("SELECT COUNT(longurl) FROM urls WHERE shorturl = '%s'" % (shorturl))
        res = conn.execute(query).fetchone()[0]
        conn.commit()

    query: Text = text("INSERT INTO urls (longurl, shorturl) VALUES ('%s','%s');" % (longurl, shorturl))

    conn.execute(query)
    conn.commit()
    conn.close()

    return {"shorturl": shorturl, "longurl": longurl}

@app.get("/use/{shorturl}", response_class=HTMLResponse)
async def redirect_user(shorturl: str):
    #Redirect the user to the long URL from the short URL
    #Add success/fails
    engine: Engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/pynyurl")
    conn: Connection = engine.connect()

    query = select(
        urls.columns.longurl
    ).where(
        urls.columns.shorturl == shorturl
    )

    res: Row[Tuple[Any]] = conn.execute(query).fetchone()
    conn.close()

    return """
    <html>
        <body>
            <script>
                    setTimeout(function(){
                        window.location.href = '%s';
                    }, 10);
            </script>
        </body>
    </html>
    """ % res[0]

if __name__ == "__main__":
   uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=True)

