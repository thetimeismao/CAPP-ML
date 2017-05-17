DROP TABLE if exists client, employer, lobbyist, connection,
    expenditures, activity, compensations;

CREATE TABLE client (
client_id int PRIMARY KEY,
name VARCHAR,
address1 VARCHAR,
address2 VARCHAR,
city VARCHAR,
state VARCHAR,
zip VARCHAR 
);

CREATE TABLE employer (
employer_id int PRIMARY KEY,
name VARCHAR,
address1 VARCHAR,
address2 VARCHAR,
city VARCHAR,
state VARCHAR,
zip VARCHAR 
);

CREATE TABLE lobbyist (
lobbyist_id int PRIMARY KEY,
lobbyist_salutation VARCHAR,
lobbyist_first_name VARCHAR,
lobbyist_last_name VARCHAR 
);

CREATE TABLE connection (
relationship_id serial PRIMARY KEY,
lobbyist_id int,
employer_id int,
client_id int
);

CREATE TABLE expenditures (
expenditure_id int PRIMARY KEY,
lobbyist_id int,
action VARCHAR,
amount numeric,
expenditure_date VARCHAR,
purpose VARCHAR,
recipient VARCHAR,
client_id int,
FOREIGN KEY (client_id)
    REFERENCES client (client_id),
FOREIGN KEY (lobbyist_id)
    REFERENCES lobbyist (lobbyist_id)
);

CREATE TABLE activity (
lobbying_activity_id int PRIMARY KEY,
client_id int,
lobbyist_id int,
action_sought VARCHAR,
department VARCHAR,
FOREIGN KEY (client_id)
    REFERENCES client (client_id),
FOREIGN KEY (lobbyist_id)
    REFERENCES lobbyist (lobbyist_id)
);

CREATE TABLE compensations (
compensation_id int PRIMARY KEY,
lobbyist_id int,
compensation_amount numeric,
client_id int,
FOREIGN KEY (client_id)
    REFERENCES client (client_id),
FOREIGN KEY (lobbyist_id)
    REFERENCES lobbyist (lobbyist_id)
);
