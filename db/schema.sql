CREATE TABLE race_meetings (
    id SERIAL PRIMARY KEY,
    meeting_date DATE,
    racecourse VARCHAR(100),
    going VARCHAR(50),
    weather VARCHAR(50)
);

CREATE TABLE races (
    id SERIAL PRIMARY KEY,
    meeting_id INT REFERENCES race_meetings(id),
    race_number INT,
    distance_m INT,
    class VARCHAR(50),
    surface VARCHAR(50)
);

CREATE TABLE horses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    sire VARCHAR(255),
    dam VARCHAR(255),
    age INT,
    sex VARCHAR(10)
);

CREATE TABLE runners (
    id SERIAL PRIMARY KEY,
    race_id INT REFERENCES races(id),
    horse_id INT REFERENCES horses(id),
    draw INT,
    weight DECIMAL,
    jockey VARCHAR(255),
    trainer VARCHAR(255),
    official_rating INT,
    form_score DECIMAL,
    finish_position INT
);

CREATE TABLE odds_history (
    id SERIAL PRIMARY KEY,
    runner_id INT REFERENCES runners(id),
    timestamp TIMESTAMP,
    decimal_odds DECIMAL,
    source VARCHAR(50)
);
