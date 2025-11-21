-- DROP TABLE IF EXISTS "users" CASCADE;
-- DROP TABLE IF EXISTS "brands" CASCADE;
-- DROP TABLE IF EXISTS "products" CASCADE;
-- DROP TABLE IF EXISTS "currencies" CASCADE;
-- DROP TABLE IF EXISTS "countries" CASCADE;
-- DROP TABLE IF EXISTS "junction_currency_country" CASCADE;
-- DROP TABLE IF EXISTS "stores" CASCADE;
-- DROP TABLE IF EXISTS "prices" CASCADE;

-- Represent every user registered in the platform
-- Count the number of its contributions to show in their profile
CREATE TABLE "users" (
    "id" SERIAL PRIMARY KEY,
    "username" VARCHAR(32) NOT NULL UNIQUE,
    "email" VARCHAR(320) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "contributions" INT DEFAULT 0,
    "deleted" BOOLEAN NOT NULL DEFAULT 'false'
    -- "avatar_url" VARCHAR(2048) UNIQUE DEFAULT 'https://pix.org/no_face.png',
    -- "avatar_image" bytea -- https://www.postgresql.org/docs/7.4/jdbc-binary-data.html
);

-- Represent the brands which make the products
CREATE TABLE "brands" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL UNIQUE,
    "website" VARCHAR(2048) NOT NULL UNIQUE,
    "inactive" BOOLEAN NOT NULL DEFAULT 'false'
);

-- Create a function to mark as discontinued a product
CREATE OR REPLACE FUNCTION discontinue_product()
RETURNS TRIGGER AS $discontinue_product$
    BEGIN
        UPDATE "products" SET "discontinued" = 'true';
    END;
$discontinue_product$ LANGUAGE plpgsql;

-- Create a trigger to call discontinue_product() when a brand is marked as inactive
CREATE OR REPLACE TRIGGER "inactive_brand"
AFTER UPDATE OF "inactive" ON "brands"
FOR EACH ROW
WHEN (OLD."inactive" = 'true')
EXECUTE FUNCTION discontinue_product();
-- in case a brand is reactivated,its products won't automatically be marked as 'reintroduced'


-- Represent any product (ingredient or ready-made), with nutriments
-- /opt/homebrew/bin/createuser per 100g in order to calculate for each recipe
CREATE TABLE "products" (
    "id" SERIAL PRIMARY KEY,
    "off_code" BIGINT UNIQUE, -- Open Food Facts database code
    "url" VARCHAR(2048) NOT NULL UNIQUE,
    "name" VARCHAR(320) NOT NULL,
    "brand_id" INT REFERENCES "brands", -- can be null if it is a simple ingredient
    "ingredients_text" TEXT NOT NULL, -- can be only one ingredient if it is a simple ingredient
    "energy" SMALLINT NOT NULL CHECK ("energy" BETWEEN 0 AND 5000), -- for 100g
    "fat" REAL NOT NULL CHECK ("fat" BETWEEN 0 AND 100), -- for 100g
    "sat_fat" REAL CHECK ("sat_fat" BETWEEN 0 AND 100), -- for 100g
    "carbs" REAL NOT NULL CHECK ("carbs" BETWEEN 0 AND 100), -- for 100g
    "sugars" REAL CHECK ("sugars" BETWEEN 0 AND 100), -- for 100g
    "fiber" REAL CHECK ("fiber" BETWEEN 0 AND 100), -- for 100g
    "protein" REAL NOT NULL CHECK ("protein" BETWEEN 0 AND 100), -- for 100g
    "sodium" REAL CHECK ("sodium" BETWEEN 0 AND 100), -- for 100g
    "c_vitamin" REAL CHECK ("c_vitamin" BETWEEN 0 AND 100), -- for 100g
    "nutr_score_fr" SMALLINT CHECK ("nutr_score_fr" BETWEEN -20 AND 50), -- https://en.wikipedia.org/wiki/Nutri-Score
    "discontinued" BOOLEAN NOT NULL DEFAULT 'false'
);

CREATE TABLE "currencies" (
    -- https://en.wikipedia.org/wiki/ISO_4217#List_of_ISO_4217_currency_codes
    "id" SMALLSERIAL PRIMARY KEY,
    "currency_name" VARCHAR(42) NOT NULL UNIQUE,
    "currency_code" VARCHAR(3) NOT NULL UNIQUE
);

CREATE TABLE "countries" (
    "id" SMALLSERIAL PRIMARY KEY,
    "country" VARCHAR(60) NOT NULL UNIQUE
);

-- junction table for a many-to-many relationship
CREATE TABLE "junction_currency_country" (
    "id" SMALLSERIAL PRIMARY KEY,
    "country_id" SMALLINT REFERENCES "countries",
    "currency_id" SMALLINT REFERENCES "currencies"
);

-- Represent the stores where the prices were seen
CREATE TABLE "stores" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "address" VARCHAR(2048) UNIQUE, -- can be null for online stores
    -- "long_lat" geography(point), -- longitude first then latitude, example: 'POINT(-118.4079 33.9434)'
    -- To use it, you must first install the PostGIS extension and then create a table with a geography(point) column, using functions like ST_GeogFromText to insert data
    "country_id" INT REFERENCES "countries", -- can be null for online stores
    "website" VARCHAR(2048) UNIQUE, -- can be null for physical stores
    "inactive" BOOLEAN NOT NULL DEFAULT 'false'
);

-- Represent the prices in cents per 100g seen for each product and their corresponding stores
-- There can be various prices according to various dates, various stores, various packaging sizes
CREATE TABLE "prices" (
    "id" BIGSERIAL PRIMARY KEY,
    "product_id" INT NOT NULL REFERENCES "products",
    "store_id" INT NOT NULL REFERENCES "stores",
    "date" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "price" SMALLINT NOT NULL CHECK ("price" >= 0), -- in cents per packaging
    "weight" INT CHECK ("weight" >= 0), -- packaging size in grams
    "quantity" INT CHECK ("quantity" >= 0), -- packaging size in units
    -- "product_pic_file" bytea, -- https://www.postgresql.org/docs/7.4/jdbc-binary-data.html
    -- "product_pic_url" VARCHAR(2048) DEFAULT 'https://pix.org/no_pic.png', -- https://prices.openfoodfacts.org/api/docs
    "currency_id" SMALLINT NOT NULL REFERENCES "currencies",
    "author_id" INT NOT NULL REFERENCES "users", -- user who uploaded the data
    "comment" VARCHAR(2048),
    "deleted" BOOLEAN NOT NULL DEFAULT 'false'
);
