from typing import Any
import uuid
import uvicorn
import urllib.parse
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import (
    Column,
    Connection,
    Engine,
    Integer,
    MetaData,
    Row,
    Sequence,
    Table,
    Text,
    Tuple,
    create_engine,
    insert,
    select,
    text,
    update,
    values,
)

POSTGRES_DB_NAME = os.environ["POSTGRES_DB_NAME"]
POSTGRES_DB_USER = os.environ["POSTGRES_DB_USER"]
POSTGRES_DB_PASS = os.environ["POSTGRES_DB_PASS"]
POSTGRES_DB_HOST = os.environ["POSTGRES_DB_HOST"]
POSTGRES_DB_PORT = os.environ["POSTGRES_DB_PORT"]
APP_HOST = os.environ["APP_HOST"]
APP_PORT = os.environ["APP_PORT"]

app = FastAPI()
metadata: MetaData = MetaData()
urls = Table(
    "urls",
    metadata,
    Column("shorturl", Text, nullable=False, primary_key=True),
    Column("longurl", Text, nullable=False),
    Column("interactions", Integer),
)


@app.get("/new/")
async def shortenURL(longurl: str):
    # This function will generate a shortened URL from a URL that a user delivers to it.
    # The new URL will be 7 characters long and random. There should be no duplicates entries.

    longurl = urllib.parse.unquote(longurl)  # maybe unneeded

    engine: Engine = create_engine(
        "postgresql+psycopg2://%s:%s@%s:%s/%s"
        % (
            POSTGRES_DB_USER,
            POSTGRES_DB_PASS,
            POSTGRES_DB_HOST,
            POSTGRES_DB_PORT,
            POSTGRES_DB_NAME,
        )
    )
    conn: Connection = engine.connect()
    shorturl: str = ""
    res: int = -1
    while res != 0:
        shorturl = uuid.uuid4().hex[
            0:7
        ]  # probably should do it better than this! placeholder
        query: Text = text(
            "SELECT COUNT(longurl) FROM urls WHERE shorturl = '%s'" % (shorturl)
        )
        res = conn.execute(query).fetchone()[0]
        conn.commit()

    query: Text = text(
        "INSERT INTO urls (longurl, shorturl) VALUES ('%s','%s');" % (longurl, shorturl)
    )

    conn.execute(query)
    conn.commit()
    conn.close()

    return {"shorturl": shorturl, "longurl": longurl}


@app.get("/use/{shorturl}", response_class=HTMLResponse)
async def redirect_user(shorturl: str):
    # This function will redirect the user to the long URL from the short URL
    # Add success/fails
    engine: Engine = create_engine(
        "postgresql+psycopg2://%s:%s@%s:%s/%s"
        % (
            POSTGRES_DB_USER,
            POSTGRES_DB_PASS,
            POSTGRES_DB_HOST,
            POSTGRES_DB_PORT,
            POSTGRES_DB_NAME,
        )
    )
    conn: Connection = engine.connect()

    query = select(urls.columns.longurl).where(urls.columns.shorturl == shorturl)

    res: Row[Tuple[Any]] = conn.execute(query).fetchone()

    query = update(urls).where(urls.columns.shorturl == shorturl).values(interactions = urls.columns.interactions + 1)
    conn.execute(query)

    conn.close()

    return (
        """
    <html>
        <body>
            <script>
                    setTimeout(function(){
                        window.location.href = '%s';
                    }, 10);
            </script>
        </body>
    </html>
    """
        % res[0]
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=True)
