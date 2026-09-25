-----------------------------------------------------
-- Données d'exemple
-----------------------------------------------------
trtllchmst
-- Utilisateurs
INSERT INTO users (username, email, password, administrator) VALUES
('alice',   'alice@mail.com',   'hashed_pwd_1', TRUE),
('bob',     'bob@mail.com',     'hashed_pwd_2', FALSE),
('chloe',   'chloe@mail.com',   'hashed_pwd_3', FALSE),
('david',   'david@mail.com',   'hashed_pwd_4', FALSE),
('emma',    'emma@mail.com',    'hashed_pwd_5', FALSE);

-- Films
INSERT INTO movies (movie_id, title, runtime, genre, plot) VALUES
(1, 'Dune: Part Two',    166, 'Science-fiction', 'Paul Atreides s'unit aux Fremen pour se venger.'),
(2, 'Oppenheimer',       180, 'Biopic',          'La vie du physicien derrière la bombe atomique.'),
(3, 'Le Fabelmans',      151, 'Drame',           'Un jeune garçon découvre sa passion pour le cinéma.'),
(4, 'Barbie',            114, 'Comédie',         'Barbie quitte Barbieland pour le monde réel.'),
(5, 'Interstellar',      169, 'Science-fiction', 'Un groupe d''explorateurs voyage à travers un trou de ver.');

-- Salles
INSERT INTO rooms (capacity) VALUES
(80),
(120),
(50);

-- Tarifs
INSERT INTO pricings (name, description, price) VALUES
('Plein tarif',   'Tarif standard adulte',        1200),
('Tarif réduit',  'Étudiants, moins de 18 ans',     900),
('Tarif senior',  'Personnes de plus de 65 ans',    950);

-- Séances (2 séances par film sur des salles différentes)
INSERT INTO screenings (movie_id, room_id, date, start_time, end_time, version, ticket_sold, revenue) VALUES
(1, 1, '2026-09-26', '2026-09-26 18:00:00+02', '2026-09-26 20:46:00+02', 'VF', 45, 54000),
(1, 2, '2026-09-27', '2026-09-27 21:00:00+02', '2026-09-27 23:46:00+02', 'VOSTFR', 60, 72000),
(2, 2, '2026-09-26', '2026-09-26 19:30:00+02', '2026-09-26 22:30:00+02', 'VOSTFR', 80, 96000),
(3, 3, '2026-09-28', '2026-09-28 17:00:00+02', '2026-09-28 19:31:00+02', 'VF', 20, 24000),
(4, 1, '2026-09-27', '2026-09-27 20:00:00+02', '2026-09-27 21:54:00+02', 'VF', 70, 84000);

-- Réservations (liens users <-> screenings <-> pricings)
INSERT INTO bookings (user_id, screening_id, pricing_id, time_of_booking) VALUES
(1, 1, 1, '2026-09-20 10:15:00+02'),
(2, 1, 2, '2026-09-21 14:00:00+02'),
(3, 3, 1, '2026-09-22 09:30:00+02'),
(4, 4, 3, '2026-09-23 16:45:00+02'),
(5, 5, 1, '2026-09-24 11:20:00+02'),
(1, 5, 2, '2026-09-24 18:00:00+02');

-- Commentaires (liens users <-> movies)
INSERT INTO comments (user_id, movie_id, content, star, spoiler) VALUES
(1, 1, 'Une suite grandiose, visuellement impressionnante.', 5, FALSE),
(2, 1, 'Un peu long mais l''ambiance est incroyable.',        4, FALSE),
(3, 2, 'Cillian Murphy est bouleversant dans ce rôle.',       5, FALSE),
(4, 3, 'Spielberg à son meilleur, très personnel.',           4, FALSE),
(5, 4, 'Drôle et plus profond qu''il n''y paraît.',           4, TRUE);

-- Films vus (liens users <-> movies)
INSERT INTO movies_watched (movie_id, user_id) VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 4),
(4, 5),
(5, 1);
