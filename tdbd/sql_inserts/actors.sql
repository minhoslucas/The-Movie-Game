SET search_path TO movies_data;

-- Movie ID: 11
INSERT INTO actor (actor_id, name) VALUES (2, 'Mark Hamill') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (3, 'Harrison Ford') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (4, 'Carrie Fisher') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (5, 'Peter Cushing') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (12248, 'Alec Guinness') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (6, 'Anthony Daniels') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (130, 'Kenny Baker') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (24343, 'Peter Mayhew') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (24342, 'David Prowse') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (15152, 'James Earl Jones') ON CONFLICT (actor_id) DO NOTHING;

-- Movie ID: 550
INSERT INTO actor (actor_id, name) VALUES (819, 'Edward Norton') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (287, 'Brad Pitt') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (1283, 'Helena Bonham Carter') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (7470, 'Meat Loaf') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (7499, 'Jared Leto') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (7471, 'Zach Grenier') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (7497, 'Holt McCallany') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (7498, 'Eion Bailey') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (7472, 'Richmond Arquette') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (7219, 'David Andrews') ON CONFLICT (actor_id) DO NOTHING;

-- Movie ID: 13
INSERT INTO actor (actor_id, name) VALUES (31, 'Tom Hanks') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (32, 'Robin Wright') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (33, 'Gary Sinise') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (35, 'Sally Field') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (34, 'Mykelti Williamson') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (37821, 'Michael Conner Humphreys') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (204997, 'Hanna Hall') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (9640, 'Haley Joel Osment') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (6751, 'Siobhan Fallon Hogan') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (3817610, 'Rebecca Williams') ON CONFLICT (actor_id) DO NOTHING;

-- Movie ID: 120
INSERT INTO actor (actor_id, name) VALUES (109, 'Elijah Wood') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (1327, 'Ian McKellen') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (110, 'Viggo Mortensen') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (1328, 'Sean Astin') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (65, 'Ian Holm') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (882, 'Liv Tyler') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (113, 'Christopher Lee') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (48, 'Sean Bean') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (1329, 'Billy Boyd') ON CONFLICT (actor_id) DO NOTHING;
INSERT INTO actor (actor_id, name) VALUES (1330, 'Dominic Monaghan') ON CONFLICT (actor_id) DO NOTHING;

