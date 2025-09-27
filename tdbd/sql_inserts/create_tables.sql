SET search_path TO movies_data;

DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

DROP TABLE IF EXISTS producer;
CREATE TABLE producer (
    producer_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    foundation_date DATE,
    origin_country VARCHAR(50)
);

DROP TABLE IF EXISTS director;
CREATE TABLE director (
    director_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    birthdate DATE,
    origin_country VARCHAR(50)
);

DROP TABLE IF EXISTS writer;
CREATE TABLE writer (
    writer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    birthdate DATE,
    origin_country VARCHAR(50)
);

DROP TABLE IF EXISTS award;
CREATE TABLE award (
    award_id SERIAL PRIMARY KEY,
    award_name VARCHAR(100) NOT NULL,
    description TEXT
);

DROP TABLE IF EXISTS actor;
CREATE TABLE actor (
    actor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birthdate DATE
);

DROP TABLE IF EXISTS genre;
CREATE TABLE genre (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(50) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS movie;
CREATE TABLE movie (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date DATE,
    duration_minutes INT,
    rating NUMERIC(3, 1),
    synopsis TEXT,
    overview TEXT,
    adult BOOLEAN DEFAULT FALSE,
    budget BIGINT,
    revenue BIGINT,
    tagline VARCHAR(255),
    producer_id INT,
    CONSTRAINT fk_producer FOREIGN KEY (producer_id) REFERENCES producer(producer_id)
);

DROP TABLE IF EXISTS today_movie;
CREATE TABLE today_movie (
    today_date DATE PRIMARY KEY,
    movie_id INT NOT NULL,
    CONSTRAINT fk_movie_id FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS guess;
CREATE TABLE guess (
    guess_id SERIAL PRIMARY KEY,
    today_date DATE NOT NULL,
    attempt_number INT NOT NULL,
    event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_today_date FOREIGN KEY (today_date) REFERENCES today_movie(today_date) ON DELETE CASCADE,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_movie_id FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    UNIQUE (today_date, user_id, attempt_number)
);

DROP TABLE IF EXISTS movie_award;
CREATE TABLE movie_award (
    movie_id INT NOT NULL,
    award_id INT NOT NULL,
    year INT NOT NULL,
    PRIMARY KEY (movie_id, award_id, year),
    CONSTRAINT fk_movie_id FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    CONSTRAINT fk_award_id FOREIGN KEY (award_id) REFERENCES award(award_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS movie_director;
CREATE TABLE movie_director (
    movie_id INT NOT NULL,
    director_id INT NOT NULL,
    PRIMARY KEY (movie_id, director_id),
    CONSTRAINT fk_movie_id FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    CONSTRAINT fk_director_id FOREIGN KEY (director_id) REFERENCES director(director_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS movie_writer;
CREATE TABLE movie_writer (
    movie_id INT NOT NULL,
    writer_id INT NOT NULL,
    PRIMARY KEY (movie_id, writer_id),
    CONSTRAINT fk_movie_id FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    CONSTRAINT fk_writer_id FOREIGN KEY (writer_id) REFERENCES writer(writer_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS acted_in;
CREATE TABLE acted_in (
    movie_id INT NOT NULL,
    actor_id INT NOT NULL,
    PRIMARY KEY (movie_id, actor_id),
    CONSTRAINT fk_movie_id FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    CONSTRAINT fk_actor_id FOREIGN KEY (actor_id) REFERENCES actor(actor_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS movie_genre;
CREATE TABLE movie_genre (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    CONSTRAINT fk_movie_id FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    CONSTRAINT fk_genre_id FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
);