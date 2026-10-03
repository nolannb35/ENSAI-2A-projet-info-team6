-----------------------------------------------------
-- Users
-----------------------------------------------------
INSERT INTO users(user_id, username, email, password, administrator) VALUES
(999, 'admin',   'admin@ensai-cinema.fr',  'admin',      TRUE),
(998, 'nolann',  'nolann@mail.fr',         'nolann123',  FALSE),
(997, 'simon',   'simon@mail.fr',          'simon123',   FALSE),
(996, 'zoeb',    'zoeb@mail.fr',           'zoeb123',    FALSE),
(995, 'samuel',  'samuel@mail.fr',         'samuel123',  FALSE);


-----------------------------------------------------
-- Movies
-----------------------------------------------------
INSERT INTO movies(movie_id, title, runtime, genre, plot) VALUES
(693134, 'Dune: Part Two',        166, 'Science-Fiction, Aventure',         'Paul Atreides s''allie aux Fremen pour venger sa famille et empêcher un avenir terrible.'),
(872585, 'Oppenheimer',           181, 'Drame, Histoire',                   'Le portrait du physicien J. Robert Oppenheimer et de la création de la bombe atomique.'),
(157336, 'Interstellar',          169, 'Aventure, Drame, Science-Fiction',  'Des explorateurs traversent un trou de ver pour trouver une nouvelle planète habitable.'),
(346698, 'Barbie',                114, 'Comédie, Aventure',                 'Barbie quitte Barbieland et découvre le monde réel.'),
(915935, 'Anatomie d''une chute', 152, 'Thriller, Drame',                   'Une écrivaine est accusée de la mort de son mari, retrouvé au pied de leur chalet.');


-----------------------------------------------------
-- Rooms
-----------------------------------------------------
INSERT INTO rooms(room_id, capacity) VALUES
(999, 90),
(998, 60),
(997, 40);


-----------------------------------------------------
-- Pricings
-----------------------------------------------------
INSERT INTO pricings(pricing_id, name, description, price) VALUES
(999, 'Plein tarif',     'Tarif normal',                     950),
(998, 'Tarif étudiant',  'Sur présentation de la carte',     700),
(997, 'Moins de 14 ans', 'Enfants de moins de 14 ans',       500),
(996, 'Tarif ENSAI',     'Élèves et personnel de l''ENSAI',  100);


-----------------------------------------------------
-- Screenings
-----------------------------------------------------
INSERT INTO screenings(screening_id, movie_id, room_id, date, start_time, end_time, version, ticket_sold, revenue) VALUES
(999, 693134, 999, '2026-09-20', '2026-09-20 18:00:00+02', '2026-09-20 20:46:00+02', 'VF',     3, 1750),
(998, 346698, 999, '2026-09-20', '2026-09-20 22:00:00+02', '2026-09-20 23:54:00+02', 'VOSTFR', 0,    0),
(997, 872585, 998, '2030-01-15', '2030-01-15 20:00:00+01', '2030-01-15 23:01:00+01', 'VOSTFR', 1,  100),
(996, 157336, 997, '2030-01-16', '2030-01-16 18:00:00+01', '2030-01-16 20:49:00+01', 'VOSTFR', 0,    0),
(995, 693134, 998, '2030-01-17', '2030-01-17 14:00:00+01', '2030-01-17 16:46:00+01', 'VF',     0,    0);


-----------------------------------------------------
-- Bookings
-----------------------------------------------------
INSERT INTO bookings(booking_id, screening_id, time_of_booking) VALUES
(999, 999, '2026-09-15 10:00:00+02'),
(998, 999, '2026-09-16 14:30:00+02'),
(997, 997, '2026-09-30 09:15:00+02');


INSERT INTO booking_user(booking_id, user_id, pricing_id) VALUES
(999, 998, 996),
(999, 997, 998),
(998, 996, 999),
(997, 995, 996);


-----------------------------------------------------
-- Comments
-----------------------------------------------------
INSERT INTO comments(comment_id, user_id, movie_id, content, star, spoiler) VALUES
(999, 998, 693134, 'Visuellement impressionnant, à voir au cinéma.',  5, FALSE),
(998, 997, 693134, 'Un peu long mais l''ambiance est incroyable.',    4, FALSE),
(997, 996, 693134, 'La fin m''a surpris, Paul change complètement.',   4, TRUE);


-----------------------------------------------------
-- Movies watched
-----------------------------------------------------
INSERT INTO movies_watched(movie_id, user_id) VALUES
(693134, 998),
(693134, 997),
(693134, 996);