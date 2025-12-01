DELETE FROM "users" CASCADE;
DELETE FROM "products" CASCADE;
DELETE FROM "brands" CASCADE;
DELETE FROM "junction_currency_country" CASCADE;
DELETE FROM "currencies" CASCADE;
DELETE FROM "stores" CASCADE;
DELETE FROM "countries" CASCADE;
DELETE FROM "prices" CASCADE;
DELETE FROM "presaved_products" CASCADE;
DELETE FROM "presaved_prices" CASCADE;

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

\COPY "brands"("name", "website") FROM 'brands.csv' delimiter ';' csv header;
-- Seeding the "products" table:
-- Create a temporary table to hold the CSV data
CREATE TEMPORARY TABLE "tmp_products" (
    "off_code" BIGINT,
    "url" VARCHAR(2048),
    "name" VARCHAR(320),
    "ingredients_text" TEXT,
    "energy" SMALLINT,
    "fat" REAL,
    "sat_fat" REAL,
    "carbs" REAL,
    "sugars" REAL,
    "fiber" REAL,
    "protein" REAL,
    "sodium" REAL,
    "c_vitamin" REAL,
    "nutr_score_fr" SMALLINT,
    "brand_name" VARCHAR(320)
);
-- Copy the CSV data into the temporary table
\COPY "tmp_products"("off_code", "url", "name", "ingredients_text", "energy", "fat", "sat_fat", "carbs", "sugars", "fiber", "protein", "sodium", "c_vitamin", "nutr_score_fr", "brand_name") FROM 'products.csv' delimiter ';' csv header;
DO $$
DECLARE
    row tmp_products%ROWTYPE;
BEGIN
    FOR row IN SELECT * FROM "tmp_products"
    LOOP
        INSERT INTO "products"("off_code", "url", "name", "brand_id", "ingredients_text", "energy", "fat", "sat_fat", "carbs", "sugars", "fiber", "protein", "sodium", "c_vitamin", "nutr_score_fr", "author_id")
        VALUES (row.off_code, row.url, row.name,
            (SELECT "id" FROM "brands" WHERE "name" = row.brand_name),
            row.ingredients_text, row.energy, row.fat, row.sat_fat, row.carbs, row.sugars, row.fiber, row.protein, row.sodium, row.c_vitamin, row.nutr_score_fr,
            (SELECT "id" FROM "users" WHERE "username" = 'Noemi')
            );
-- author_id always set to Noemi with this seed file
    END LOOP;
END $$;
DROP TABLE "tmp_products";

\COPY "currencies"("currency_name", "currency_code") FROM 'currencies.csv' delimiter ';' csv header;
\COPY "countries"("country") FROM 'countries.csv' delimiter ';' csv header;

-- Seeding the "junction_currency_country" junction table:
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

INSERT INTO "stores" ("name", "address", "website", "country_id", "author_id") VALUES
('Consum', 'Carrer de València, 478, L''Eixample, 08013 Barcelona', 'https://www.consum.es/', (
    SELECT "id" FROM "countries" WHERE "country" = 'SPAIN'
), (SELECT "id" FROM "users" WHERE "username" = 'Noemi')),
-- author_id always set to Noemi with this seed file
('Carrefour', 'Westfield Las Glorias, Calle Les Glories, esquina Calle Llacunna, 155, Av. Diagonal, 208, Centro Comercial, 08018 Barcelona', 'https://www.carrefour.es/tiendas-carrefour/hipermercados/carrefour/las_glorias.aspx', (
    SELECT "id" FROM "countries" WHERE "country" = 'SPAIN'
), (SELECT "id" FROM "users" WHERE "username" = 'Noemi')),
('Mercadona', 'Carrer del Perú, 151, Sant Martí, 08018 Barcelona', 'http://mercadona.es/', (
    SELECT "id" FROM "countries" WHERE "country" = 'SPAIN'
), (SELECT "id" FROM "users" WHERE "username" = 'Noemi'));

-- seeding prices with random values
DO $$
DECLARE
    row products%ROWTYPE;
BEGIN
    FOR row IN SELECT * FROM "products"
    LOOP
        INSERT INTO "prices" ("product_id","store_id","price","weight","quantity","currency_id","author_id","comment")
        VALUES (
            (SELECT "id" FROM "products" WHERE "off_code" = row.off_code),
            (SELECT "id" FROM "stores" WHERE "name" = 'Carrefour'),
            (trunc((random()*798) + 201)),
            (trunc((random()*399) + 101)),
            1,
            (SELECT "id" FROM "currencies" WHERE "currency_code" = 'USD'),
            (SELECT "id" FROM "users" WHERE "username" = 'Noemi'),
            'Random testing value');
    END LOOP;
END $$;
