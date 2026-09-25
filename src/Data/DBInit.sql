-----------------------------------------------------
-- Player
-----------------------------------------------------

DROP TABLE IF EXISTS player CASCADE;
CREATE TABLE bookings (
    booking_id    SERIAL PRIMARY KEY,
    user_id      INTEGER REFERENCES users(user_id),
    screening_id    INTEGER REFERENCES screenings(screening_id),
    pricing_id    INTEGER REFERENCES pricings(pricing_id),
    time_of_booking TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE movies (
    id_movie      INTEGER,
    title         VARCHAR(1024),
    runtime        INTEGER,
    genre         VARCHAR(564)
    plot          VARCHAR(1024)
);

CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    movie_id INTEGER REFERENCES movies(movie_id),
    content VARCHAR(2048,
    star INTEGER,
    spoiler BIT,
);

CREATE TABLE movies_watched (
    movie_id REFERENCES movies(movie_id),
    user_id REFERENCES users(user_id)
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(32),
    email VARCHAR,
    password VARCHAR,
    administrator BIT
);

CREATE TABLE rooms (
    room_id SMALLINT,
    capacity SMALLINT
)