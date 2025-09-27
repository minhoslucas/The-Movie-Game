SET search_path TO movies_data;

-- Movie ID: 11
INSERT INTO genre (genre_id, genre_name) VALUES (12, 'Adventure') ON CONFLICT (genre_id) DO NOTHING;
INSERT INTO genre (genre_id, genre_name) VALUES (28, 'Action') ON CONFLICT (genre_id) DO NOTHING;
INSERT INTO genre (genre_id, genre_name) VALUES (878, 'Science Fiction') ON CONFLICT (genre_id) DO NOTHING;

-- Movie ID: 550
INSERT INTO genre (genre_id, genre_name) VALUES (18, 'Drama') ON CONFLICT (genre_id) DO NOTHING;
INSERT INTO genre (genre_id, genre_name) VALUES (53, 'Thriller') ON CONFLICT (genre_id) DO NOTHING;

-- Movie ID: 13
INSERT INTO genre (genre_id, genre_name) VALUES (35, 'Comedy') ON CONFLICT (genre_id) DO NOTHING;
INSERT INTO genre (genre_id, genre_name) VALUES (18, 'Drama') ON CONFLICT (genre_id) DO NOTHING;
INSERT INTO genre (genre_id, genre_name) VALUES (10749, 'Romance') ON CONFLICT (genre_id) DO NOTHING;

-- Movie ID: 120
INSERT INTO genre (genre_id, genre_name) VALUES (12, 'Adventure') ON CONFLICT (genre_id) DO NOTHING;
INSERT INTO genre (genre_id, genre_name) VALUES (14, 'Fantasy') ON CONFLICT (genre_id) DO NOTHING;
INSERT INTO genre (genre_id, genre_name) VALUES (28, 'Action') ON CONFLICT (genre_id) DO NOTHING;

