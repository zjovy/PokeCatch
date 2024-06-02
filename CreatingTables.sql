CREATE DATABASE pokecatch;
USE pokecatch;

DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS pokeballs;
DROP TABLE IF EXISTS pokemons;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    userid VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255)
);

CREATE TABLE pokemons (
    pokemonid INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sprite VARCHAR(255),
    type VARCHAR(255),
    region VARCHAR(255),
    encounter_rate INT NOT NULL
);

CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userid VARCHAR(255) NOT NULL,
    pokemonid INT NOT NULL,
    FOREIGN KEY (userid) REFERENCES users(userid),
    FOREIGN KEY (pokemonid) REFERENCES pokemons(pokemonid)
);

CREATE TABLE pokeballs (
    userid VARCHAR(255),
    ballcount INT NOT NULL,
    FOREIGN KEY (userid) REFERENCES users(userid)
);

-- SELECT * from users;
-- SELECT * from pokeballs;
-- SELECT * from pokemons;
-- SELECT * from inventory
