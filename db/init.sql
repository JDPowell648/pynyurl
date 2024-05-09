CREATE DATABASE pynyurl;
GRANT ALL PRIVILEGES ON DATABASE pynyurl TO postgres;
\connect pynyurl;

CREATE TABLE urls (
    shorturl text NOT NULL,
    longurl text NOT NULL,
    interactions int,
    PRIMARY KEY (shorturl)
);