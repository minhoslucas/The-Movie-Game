SET search_path TO movies_data;

-- Movie ID: 11
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (1, 'Lucasfilm Ltd.', 'US') ON CONFLICT (producer_id) DO NOTHING;
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (25, '20th Century Fox', 'US') ON CONFLICT (producer_id) DO NOTHING;

-- Movie ID: 550
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (711, 'Fox 2000 Pictures', 'US') ON CONFLICT (producer_id) DO NOTHING;
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (508, 'Regency Enterprises', 'US') ON CONFLICT (producer_id) DO NOTHING;
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (4700, 'Linson Entertainment', 'US') ON CONFLICT (producer_id) DO NOTHING;
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (25, '20th Century Fox', 'US') ON CONFLICT (producer_id) DO NOTHING;
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (20555, 'Taurus Film', 'DE') ON CONFLICT (producer_id) DO NOTHING;

-- Movie ID: 13
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (4, 'Paramount Pictures', 'US') ON CONFLICT (producer_id) DO NOTHING;
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (21920, 'The Steve Tisch Company', 'US') ON CONFLICT (producer_id) DO NOTHING;
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (412, 'Wendy Finerman Productions', '') ON CONFLICT (producer_id) DO NOTHING;

-- Movie ID: 120
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (12, 'New Line Cinema', 'US') ON CONFLICT (producer_id) DO NOTHING;
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (11, 'WingNut Films', 'NZ') ON CONFLICT (producer_id) DO NOTHING;
INSERT INTO producer (producer_id, company_name, origin_country) VALUES (5237, 'The Saul Zaentz Company', 'US') ON CONFLICT (producer_id) DO NOTHING;

