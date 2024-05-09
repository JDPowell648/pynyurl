CREATE DATABASE pynyurl;
USE pynyurl
GRANT ALL PRIVILEGES ON DATABASE pynyurl TO postgres;

CREATE TABLE urls
(
    shortURL text NOT NULL,
    longURL text NOT NULL,
    interactions int,
    PRIMARY KEY (shortURL)
);

INSERT INTO urls (shortURL, longURL, interactions)
VALUES (test, test, 0); 