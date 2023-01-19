

CREATE TABLE IF NOT EXISTS clients(
    client_id SERIAL PRIMARY KEY NOT NULL,
    first_name VARCHAR(120),
    last_name VARCHAR(120),
    e_mail VARCHAR(120) -- :?D

);

CREATE TABLE IF NOT EXISTS clients_phones_dep(
client_id INTEGER NOT NULL REFERENCES clients(client_id),
client_phone BIGINT NOT NULL,
CONSTRAINT idp_pk PRIMARY KEY (client_id, client_phone)
);

INSERT INTO clients(first_name, last_name, e_mail)
VALUES('test1', 'test1 last name', 'e-mail')
RETURNING client_id;