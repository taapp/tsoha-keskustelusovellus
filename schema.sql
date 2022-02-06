CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    created_at TIMESTAMP,
    is_admin BOOLEAN,
    is_visible BOOLEAN
);
CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    name TEXT,
    created_at TIMESTAMP,
    is_secret BOOLEAN,
    is_visible BOOLEAN
);
CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    area_id INTEGER REFERENCES areas,
    title TEXT,
    created_at TIMESTAMP,
    is_visible BOOLEAN
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads,
    content TEXT,
    created_at TIMESTAMP,
    is_visible BOOLEAN
);
CREATE TABLE users_areas (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    area_id INTEGER REFERENCES areas
);