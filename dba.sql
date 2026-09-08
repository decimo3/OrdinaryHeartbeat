CREATE TABLE IF NOT EXISTS heartbeat (
    identifier SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    created_by VARCHAR(30) NOT NULL,
    creator_ip VARCHAR(30) NOT NULL,
    creator_ver VARCHAR(10) NOT NULL
);

