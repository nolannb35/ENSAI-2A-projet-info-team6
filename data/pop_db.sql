INSERT INTO users(username, email, password, administrator) VALUES
('admin',  'admin@ensai.fr',  'admin',  TRUE),
('alice',  'alice@mail.com',  '1234',   FALSE),
('bob',    'bob@mail.com',    'abcd',   FALSE),
('chloe',  'chloe@mail.com',  'azerty', FALSE),
('david',  'david@mail.com',  'toto',   FALSE),
('emma',   'emma@mail.com',   'emma',   FALSE);


INSERT INTO movies(movie_id, title, runtime, genre, plot) VALUES
(693134, 'Dune: Part Two', 166, 'Science-fiction', 'Paul Atreides s''unit aux Fremen pour se venger.'),
(872585, 'Oppenheimer',    180, 'Biopic',          'La vie du physicien derrière la bombe atomique.'),
(804095, 'Le Fabelmans',   151, 'Drame',           'Un jeune garçon découvre sa passion pour le cinéma.'),
(346698, 'Barbie',         114, 'Comédie',         'Barbie quitte Barbieland pour le monde réel.'),
(157336, 'Interstellar',   169, 'Science-fiction', 'Un groupe d''explorateurs voyage à travers un trou de ver.');


INSERT INTO rooms(capacity) VALUES
(80),
(120),
(50);


INSERT INTO pricings(name, description, price) VALUES
('Plein tarif',  'Tarif standard adulte',       1200),
('Tarif réduit', 'Étudiants, moins de 18 ans',   900),
('Tarif senior', 'Personnes de plus de 65 ans',  950);


INSERT INTO screenings(movie_id, room_id, date, start_time, end_time, version) VALUES
(693134, 1, '2026-10-02', '2026-10-02 18:00:00+02', '2026-10-02 20:46:00+02', 'VF'),
(693134, 2, '2026-10-03', '2026-10-03 21:00:00+02', '2026-10-03 23:46:00+02', 'VOSTFR'),
(872585, 2, '2026-10-02', '2026-10-02 17:30:00+02', '2026-10-02 20:30:00+02', 'VOSTFR'),
(804095, 3, '2026-10-04', '2026-10-04 17:00:00+02', '2026-10-04 19:31:00+02', 'VF'),
(346698, 1, '2026-10-03', '2026-10-03 20:00:00+02', '2026-10-03 21:54:00+02', 'VF');