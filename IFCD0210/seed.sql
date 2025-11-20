DELETE FROM "users" CASCADE;
DELETE FROM "junction_currency_country" CASCADE;
DELETE FROM "countries" CASCADE;
DELETE FROM "currencies" CASCADE;

INSERT INTO "users" ("username", "email", "password") VALUES
('Noemi', 'noemi@gmail.com', 'password'),
('Rossana', 'rossana@gmail.com', 'password'),
('Maria', 'maria@gmail.com', 'password'),
('Juan', 'juan@gmail.com', 'password');



-- Calling a .csv file from a python script to pgsql is quite complex and
-- not very effective, here is the only way to do it (tried lots of other):
--  https://www.oneschema.co/blog/import-csv-postgresql
-- Therefore, simply read this seed.sql file directly from the psql client.

-- COPY is run by the Postgres server, and the path is relative to the server
-- path, or absolute, but on the server machine. If you want to use a path
-- from client, use \COPY, which is a psql's command.

-- COPY with a file name instructs the PostgreSQL server to directly read from
-- or write to a file. The file must be accessible to the server and the name
-- must be specified from the viewpoint of the server. When STDIN or STDOUT is
-- specified, data is transmitted via the connection between the client and
-- the server.

\COPY "countries"("country") FROM 'countries.csv' delimiter ';' csv header;
\COPY "currencies"("currency_name", "currency_code") FROM 'currencies.csv' delimiter ';' csv header;
\COPY "brands"("name", "website") FROM 'brands.csv' delimiter ';' csv header;

-- seed the "junction_curren_countr" junction table:
-- Create a temporary table to hold the CSV data
CREATE TEMPORARY TABLE "tmp_junction" (
    "country" TEXT,
    "currency_code" TEXT
);
-- Copy the CSV data into the temporary table
\COPY "tmp_junction"("country", "currency_code") FROM 'junction_currency_country.csv' WITH DELIMITER ';' CSV HEADER;
-- Iterate over the temporary table using a loop
DO $$
DECLARE
    row tmp_junction%ROWTYPE;
BEGIN
    FOR row IN SELECT * FROM "tmp_junction"
    LOOP
        INSERT INTO "junction_currency_country" ("country_id", "currency_id")
        VALUES (
            (SELECT id FROM countries WHERE country = row.country),
            (SELECT id FROM currencies WHERE currency_code = row.currency_code)
        );
    END LOOP;
END $$;
DROP TABLE "tmp_junction";


