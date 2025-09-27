SET search_path TO movies_data;

-- Movie ID: 11
INSERT INTO director (director_id, full_name) VALUES (1, 'George Lucas') ON CONFLICT (director_id) DO NOTHING;

-- Movie ID: 550
INSERT INTO director (director_id, full_name) VALUES (7467, 'David Fincher') ON CONFLICT (director_id) DO NOTHING;

-- Movie ID: 13
INSERT INTO director (director_id, full_name) VALUES (24, 'Robert Zemeckis') ON CONFLICT (director_id) DO NOTHING;

-- Movie ID: 120
INSERT INTO director (director_id, full_name) VALUES (108, 'Peter Jackson') ON CONFLICT (director_id) DO NOTHING;

