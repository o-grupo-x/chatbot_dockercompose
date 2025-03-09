CREATE TABLE "user" (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL
);

CREATE TABLE chat_session (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES "user"(id),
    name VARCHAR NOT NULL,
    model VARCHAR NOT NULL
);

CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR NOT NULL REFERENCES chat_session(id),
    sender VARCHAR NOT NULL,
    content TEXT NOT NULL
);