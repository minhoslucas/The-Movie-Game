SET search_path TO movies_data;

-- Movie ID: 11
INSERT INTO writer (writer_id, full_name) VALUES (1, 'George Lucas') ON CONFLICT (writer_id) DO NOTHING;

-- Movie ID: 550
INSERT INTO writer (writer_id, full_name) VALUES (7469, 'Jim Uhls') ON CONFLICT (writer_id) DO NOTHING;

-- Movie ID: 13
INSERT INTO writer (writer_id, full_name) VALUES (27, 'Eric Roth') ON CONFLICT (writer_id) DO NOTHING;

-- Movie ID: 120
INSERT INTO writer (writer_id, full_name) VALUES (128, 'Philippa Boyens') ON CONFLICT (writer_id) DO NOTHING;
INSERT INTO writer (writer_id, full_name) VALUES (126, 'Fran Walsh') ON CONFLICT (writer_id) DO NOTHING;
INSERT INTO writer (writer_id, full_name) VALUES (108, 'Peter Jackson') ON CONFLICT (writer_id) DO NOTHING;

