-----------------------------------------------------
-- Initialisation à 0 de la base de données
-----------------------------------------------------

-- Ordre inverse de création pour respecter les dépendances FK
DROP TABLE IF EXISTS movies_watched CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS screenings CASCADE;
DROP TABLE IF EXISTS pricings CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-----------------------------------------------------
-- Tables sans dépendances
-----------------------------------------------------

CREATE TABLE users (
    user_id        SERIAL PRIMARY KEY,
    username       TEXT NOT NULL,
    email          TEXT NOT NULL UNIQUE,
    password       TEXT NOT NULL,
    administrator  BOOLEAN DEFAULT FALSE
);

CREATE TABLE movies (
    movie_id  INTEGER NOT NULL,
    title     TEXT NOT NULL,
    runtime   INTEGER NOT NULL,
    genre     TEXT,
    plot      TEXT
);

CREATE TABLE rooms (
    room_id   SERIAL PRIMARY KEY,
    capacity  SMALLINT
);

CREATE TABLE pricings (
    pricing_id   SERIAL PRIMARY KEY,
    name         TEXT NOT NULL,
    description  TEXT,
    price        INTEGER NOT NULL
);

-----------------------------------------------------
-- Tables dépendantes (niveau 1)
-----------------------------------------------------

CREATE TABLE screenings (
    screening_id  SERIAL PRIMARY KEY,
    movie_id      INTEGER REFERENCES movies(movie_id),
    room_id       INTEGER REFERENCES rooms(room_id),
    date          DATE,
    start_time    TIMESTAMPTZ,
    end_time      TIMESTAMPTZ,
    version       TEXT,
    ticket_sold   SMALLINT DEFAULT 0,
    revenue       INTEGER DEFAULT 0
);

-----------------------------------------------------
-- Tables dépendantes (niveau 2)
-----------------------------------------------------

CREATE TABLE bookings (
    booking_id       SERIAL PRIMARY KEY,
    user_id          INTEGER REFERENCES users(user_id),
    screening_id     INTEGER REFERENCES screenings(screening_id),
    pricing_id       INTEGER REFERENCES pricings(pricing_id),
    time_of_booking  TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
    comment_id  SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES users(user_id),
    movie_id    INTEGER REFERENCES movies(movie_id),
    content     TEXT,
    star        SMALLINT CHECK (star BETWEEN 1 AND 5),
    spoiler     BOOLEAN DEFAULT FALSE
);

CREATE TABLE movies_watched (
    movie_id  INTEGER REFERENCES movies(movie_id),
    user_id   INTEGER REFERENCES users(user_id),
    PRIMARY KEY (movie_id, user_id)
);
