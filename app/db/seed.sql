DELETE FROM "users" CASCADE;
DELETE FROM "products" CASCADE;
DELETE FROM "brands" CASCADE;
DELETE FROM "junction_currency_country" CASCADE;
DELETE FROM "currencies" CASCADE;
DELETE FROM "stores" CASCADE;
DELETE FROM "countries" CASCADE;
DELETE FROM "prices" CASCADE;

INSERT INTO "users" ("username", "email", "password") VALUES
('Noemi', 'noemi@gmail.com', 'password'),
('Rossana', 'rossana@gmail.com', 'password'),
('Maria', 'maria@gmail.com', 'password'),
('Juan', 'juan@gmail.com', 'password');

-- CSV_IMPORT: brands.csv|brands|name,website|;

-- Seeding the "products" table:
-- Command 1: Create the temporary table
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
-- Command 2 (Handled by Python): Copy the CSV data into the temporary table
-- CSV_IMPORT: products.csv|tmp_products|off_code,url,name,ingredients_text,energy,fat,sat_fat,carbs,sugars,fiber,protein,sodium,c_vitamin,nutr_score_fr,brand_name|;

-- Command 3: Insert data and drop table
DO $$
DECLARE
    row tmp_products%ROWTYPE;
BEGIN
    FOR row IN SELECT * FROM "tmp_products"
    LOOP
        INSERT INTO "products"("off_code", "url", "name", "brand_id", "ingredients_text", "energy", "fat", "sat_fat", "carbs", "sugars", "fiber", "protein", "sodium", "c_vitamin", "nutr_score_fr")
        VALUES (row.off_code, row.url, row.name,
            (SELECT "id" FROM "brands" WHERE "name" = row.brand_name),
            row.ingredients_text, row.energy, row.fat, row.sat_fat, row.carbs, row.sugars, row.fiber, row.protein, row.sodium, row.c_vitamin, row.nutr_score_fr
            );
    END LOOP;
    DROP TABLE "tmp_products";
END $$;


-- CSV_IMPORT: currencies.csv|currencies|currency_name,currency_code|;
-- CSV_IMPORT: countries.csv|countries|country|;

-- Seeding the "junction_currency_country" junction table:
-- Command 1: Create the temporary table
CREATE TEMPORARY TABLE "tmp_junction" (
    "country" TEXT,
    "currency_code" TEXT
);
-- Command 2 (Handled by Python): Copy the CSV data into the temporary table
-- CSV_IMPORT: junction_currency_country.csv|tmp_junction|country,currency_code|;

-- Command 3: Iterate over the temporary table using a loop and drop it (one single block/command)
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

    -- Cleanup is placed inside the single DO block
    DROP TABLE "tmp_junction";
END $$;


INSERT INTO "stores" ("name", "address", "website", "country_id") VALUES
('Consum', 'Carrer de València, 478, L''Eixample, 08013 Barcelona', 'https://www.consum.es/', (
    SELECT "id" FROM "countries" WHERE "country" = 'SPAIN'
)),
('Carrefour', 'Westfield Las Glorias, Calle Les Glories, esquina Calle Llacunna, 155, Av. Diagonal, 208, Centro Comercial, 08018 Barcelona', 'https://www.carrefour.es/tiendas-carrefour/hipermercados/carrefour/las_glorias.aspx', (
    SELECT "id" FROM "countries" WHERE "country" = 'SPAIN'
)),
('Mercadona', 'Carrer del Perú, 151, Sant Martí, 08018 Barcelona', 'http://mercadona.es/', (
    SELECT "id" FROM "countries" WHERE "country" = 'SPAIN'
));

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
            (trunc(random()*999)),
            (trunc(random()*500)),
            1,
            (SELECT "id" FROM "currencies" WHERE "currency_code" = 'USD'),
            (SELECT "id" FROM "users" WHERE "username" = 'Noemi'),
            'Random testing value');
    END LOOP;
END $$;