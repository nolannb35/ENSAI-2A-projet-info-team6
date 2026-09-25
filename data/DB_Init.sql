-----------------------------------------------------
-- Player
-----------------------------------------------------

DROP TABLE IF EXISTS player CASCADE;
CREATE TABLE bookings (
    booking_id    SERIAL PRIMARY KEY,
    user_id      INTEGER REFERENCES users(user_id),
    screening_id    INTEGER REFERENCES screenings(screening_id),
    pricing_id    INTEGER REFERENCES pricings(pricing_id),
    time_of_booking TIMESTAMPZ DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE movies (
    id_movie      INTEGER,
    title         TEXT,
    runtime       INTEGER,
    genre         TEXT,
    plot          TEXT
);

CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    movie_id INTEGER REFERENCES movies(movie_id),
    content TEXT,
    star SMALLINT,
    spoiler BIT,
);

CREATE TABLE movies_watched (
    movie_id REFERENCES movies(movie_id),
    user_id REFERENCES users(user_id)
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT,
    email TEXT,
    password TEXT,
    administrator BIT
);

CREATE TABLE rooms (
    room_id SMALLINT,
    capacity SMALLINT
);

CREATE TABLE screenings (
    screening_id SERIAL PRIMARY KEY,
    movie_id REFERENCES movies(movie_id),
    room_id REFERENCES rooms(room_id),
    date TIMESTAMPZ,
    running Intervam
);



