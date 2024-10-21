CREATE TABLE sensor_reading (
    id SERIAL PRIMARY KEY,
    location text NOT NULL,
    timestamp timestamp NOT NULL,
    type text NOT NULL,
    value decimal NOT NULL
);
