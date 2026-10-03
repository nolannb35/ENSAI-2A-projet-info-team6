-----------------------------------------------------
-- Ensai Cinema Club : données de l'application
-----------------------------------------------------


-- Users
INSERT INTO users(username, email, password, administrator) VALUES
('admin',   'admin@ensai-cinema.fr',  'admin',      TRUE),
('nolann',  'nolann@mail.fr',         'nolann123',  FALSE),
('simon',   'simon@mail.fr',          'simon123',   FALSE),
('zoeb',    'zoeb@mail.fr',           'zoeb123',    FALSE),
('samuel',  'samuel@mail.fr',         'samuel123',  FALSE);



-- Movies
INSERT INTO movies(movie_id, title, runtime, genre, plot) VALUES
(693134, 'Dune: Part Two',                      166, 'Science-Fiction, Aventure',               'Paul Atreides s''allie aux Fremen pour venger sa famille et empêcher un avenir terrible.'),
(872585, 'Oppenheimer',                         181, 'Drame, Histoire',                         'Le portrait du physicien J. Robert Oppenheimer et de la création de la bombe atomique.'),
(157336, 'Interstellar',                        169, 'Aventure, Drame, Science-Fiction',        'Des explorateurs traversent un trou de ver pour trouver une nouvelle planète habitable.'),
(346698, 'Barbie',                              114, 'Comédie, Aventure',                       'Barbie quitte Barbieland et découvre le monde réel.'),
(569094, 'Spider-Man: Across the Spider-Verse', 140, 'Animation, Action, Aventure, Science-Fiction', 'Miles Morales voyage à travers le multivers et rencontre d''autres Spider-Men.'),
(915935, 'Anatomie d''une chute',               152, 'Thriller, Drame',                         'Une écrivaine est accusée de la mort de son mari, retrouvé au pied de leur chalet.');



-- Rooms
INSERT INTO rooms(capacity) VALUES
(90),
(60),
(40);



-- Pricings
INSERT INTO pricings(name, description, price) VALUES
('Plein tarif',     'Tarif normal',                  950),
('Tarif étudiant',  'Sur présentation de la carte',  700),
('Moins de 14 ans', 'Enfants de moins de 14 ans',    500),
('ENSAI', 'Personnel et élève de l''ENSAI',          100);



-- Screenings
INSERT INTO screenings(movie_id, room_id, date, start_time, end_time, version) VALUES
(693134, 1, '2026-10-14', '2026-10-14 18:00:00+02', '2026-10-14 20:46:00+02', 'VF'),
(346698, 1, '2026-10-14', '2026-10-14 22:00:00+02', '2026-10-14 23:54:00+02', 'VOSTFR'),
(872585, 3, '2026-10-15', '2026-10-15 20:00:00+02', '2026-10-15 23:01:00+02', 'VOSTFR'),
(915935, 2, '2026-10-16', '2026-10-16 20:00:00+02', '2026-10-16 22:32:00+02', 'VF'),
(569094, 1, '2026-10-17', '2026-10-17 14:00:00+02', '2026-10-17 16:20:00+02', 'VF'),
(157336, 1, '2026-10-17', '2026-10-17 17:30:00+02', '2026-10-17 20:19:00+02', 'VOSTFR'),
(346698, 2, '2026-10-17', '2026-10-17 20:30:00+02', '2026-10-17 22:24:00+02', 'VF'),
(569094, 2, '2026-10-18', '2026-10-18 15:00:00+02', '2026-10-18 17:20:00+02', 'VF'),
(872585, 1, '2026-10-18', '2026-10-18 20:00:00+02', '2026-10-18 23:01:00+02', 'VF'),
(157336, 3, '2026-10-31', '2026-10-31 18:00:00+01', '2026-10-31 20:49:00+01', 'VOSTFR'),
(693134, 3, '2026-11-01', '2026-11-01 16:00:00+01', '2026-11-01 18:46:00+01', 'VOSTFR');