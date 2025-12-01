DROP TABLE IF EXISTS "users" CASCADE;
DROP TABLE IF EXISTS "brands" CASCADE;
DROP TABLE IF EXISTS "products" CASCADE;
DROP TABLE IF EXISTS "currencies" CASCADE;
DROP TABLE IF EXISTS "countries" CASCADE;
DROP TABLE IF EXISTS "junction_currency_country" CASCADE;
DROP TABLE IF EXISTS "stores" CASCADE;
DROP TABLE IF EXISTS "prices" CASCADE;
DROP TABLE IF EXISTS "incomplete_products" CASCADE;
DROP TABLE IF EXISTS "incomplete_prices" CASCADE;

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

-- Create a function to mark products as discontinued for a specific brand
CREATE OR REPLACE FUNCTION discontinue_product()
RETURNS TRIGGER AS $discontinue_product$
    BEGIN
        -- Update products belonging to the brand that was marked inactive
        UPDATE "products"
        SET "discontinued" = 'true'
        WHERE "brand_id" = NEW."id";
        RETURN NEW;
    END;
$discontinue_product$ LANGUAGE plpgsql;

-- Create a trigger to call discontinue_product() when a brand is marked as inactive
CREATE OR REPLACE TRIGGER "inactive_brand"
AFTER UPDATE OF "inactive" ON "brands"
FOR EACH ROW
-- Trigger only fires when a brand is being marked inactive (not when it's already inactive):
WHEN (NEW."inactive" = 'true' AND OLD."inactive" = 'false')
EXECUTE FUNCTION discontinue_product();
-- in case a brand is reactivated,its products won't automatically be marked as 'reintroduced'


-- Represent any product (ingredient or ready-made), with nutriments per 100g in order to calculate for each recipe
CREATE TABLE "products" (
    "id" SERIAL PRIMARY KEY,
    "off_code" BIGINT UNIQUE, -- Open Food Facts database code
    "url" VARCHAR(2048) NOT NULL,
    "name" VARCHAR(320) NOT NULL,
    "brand_id" INT REFERENCES "brands", -- can be null if it is a simple ingredient
    "energy" SMALLINT NOT NULL CHECK ("energy" BETWEEN 0 AND 5000), -- for 100g
    "protein" REAL NOT NULL CHECK ("protein" BETWEEN 0 AND 100), -- for 100g
    "fat" REAL NOT NULL CHECK ("fat" BETWEEN 0 AND 100), -- for 100g
    "sat_fat" REAL CHECK ("sat_fat" BETWEEN 0 AND 100), -- for 100g
    "carbs" REAL NOT NULL CHECK ("carbs" BETWEEN 0 AND 100), -- for 100g
    "sugars" REAL CHECK ("sugars" BETWEEN 0 AND 100), -- for 100g
    "fiber" REAL CHECK ("fiber" BETWEEN 0 AND 100), -- for 100g
    "sodium" REAL CHECK ("sodium" BETWEEN 0 AND 100), -- for 100g
    "c_vitamin" REAL CHECK ("c_vitamin" BETWEEN 0 AND 100), -- for 100g
    "nutr_score_fr" SMALLINT CHECK ("nutr_score_fr" BETWEEN -20 AND 50), -- https://en.wikipedia.org/wiki/Nutri-Score
    "ingredients_text" TEXT NOT NULL, -- can be only one ingredient if it is a simple ingredient
    "author_id" INT NOT NULL REFERENCES "users", -- user who inserted the data
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
    "author_id" INT NOT NULL REFERENCES "users", -- user who inserted the data
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
    -- Weight OR quantity
    "quantity" INT CHECK ("quantity" >= 0), -- packaging size in units
    -- "product_pic_file" bytea, -- https://www.postgresql.org/docs/7.4/jdbc-binary-data.html
    -- "product_pic_url" VARCHAR(2048) DEFAULT 'https://pix.org/no_pic.png', -- https://prices.openfoodfacts.org/api/docs
    "currency_id" SMALLINT NOT NULL REFERENCES "currencies",
    "author_id" INT NOT NULL REFERENCES "users", -- user who inserted the data
    "comment" VARCHAR(2048),
    "deleted" BOOLEAN NOT NULL DEFAULT 'false'
);

-- incomplete_products
CREATE TABLE "incomplete_products" (
    "id" SERIAL PRIMARY KEY,
    "author_id" INT NOT NULL REFERENCES "users", -- user who inserted the data
    "product_url" VARCHAR(2048) UNIQUE,
    "product_name" VARCHAR(320) NOT NULL UNIQUE,
    "brand_id" INT REFERENCES "brands", -- can be null if it is a simple ingredient
    "brand_name" VARCHAR(64),
    "brand_website" VARCHAR(2048),
    "product_energy" SMALLINT CHECK ("product_energy" BETWEEN 0 AND 5000), -- for 100g
    "product_protein" REAL CHECK ("product_protein" BETWEEN 0 AND 100), -- for 100g
    "product_fat" REAL CHECK ("product_fat" BETWEEN 0 AND 100), -- for 100g
    "product_sat_fat" REAL CHECK ("product_sat_fat" BETWEEN 0 AND 100), -- for 100g
    "product_carbs" REAL CHECK ("product_carbs" BETWEEN 0 AND 100), -- for 100g
    "product_sugars" REAL CHECK ("product_sugars" BETWEEN 0 AND 100), -- for 100g
    "product_fiber" REAL CHECK ("product_fiber" BETWEEN 0 AND 100), -- for 100g
    "product_sodium" REAL CHECK ("product_sodium" BETWEEN 0 AND 100), -- for 100g
    "product_c_vitamin" REAL CHECK ("product_c_vitamin" BETWEEN 0 AND 100), -- for 100g
    "product_ingredients" TEXT, -- can be only one ingredient if it is a simple ingredient
    "completed" BOOLEAN NOT NULL DEFAULT 'false'
);

-- Create a function to insert a product into the products table
CREATE OR REPLACE FUNCTION insert_product()
RETURNS TRIGGER AS $insert_product$
    BEGIN
        INSERT INTO "products" (
            "url",
            "name",
            "brand_id",
            "energy",
            "protein",
            "fat",
            "sat_fat",
            "carbs",
            "sugars",
            "fiber",
            "sodium",
            "c_vitamin",
            "ingredients_text",
            "author_id"
        )
        VALUES (
            NEW."product_url",
            NEW."product_name",
            NEW."brand_id",
            NEW."product_energy",
            NEW."product_protein",
            NEW."product_fat",
            NEW."product_sat_fat",
            NEW."product_carbs",
            NEW."product_sugars",
            NEW."product_fiber",
            NEW."product_sodium",
            NEW."product_c_vitamin",
            NEW."product_ingredients",
            NEW."author_id"
        );

        RETURN NEW;
    END;
$insert_product$ LANGUAGE plpgsql;

-- Create a trigger to call insert_product() when an incomplete_products entry is being marked as "completed"
CREATE OR REPLACE TRIGGER "completed_product"
AFTER UPDATE OF "completed" ON "incomplete_products"
FOR EACH ROW
-- The trigger only fires when a product is being marked completed (not when it was already completed):
WHEN (NEW."completed" = 'true' AND OLD."completed" = 'false')
EXECUTE FUNCTION insert_product();
-- Create a function to mark incomplete_product as completed
CREATE OR REPLACE FUNCTION mark_incomplete_as_completed()
RETURNS TRIGGER AS $mark_incomplete_as_completed$
    BEGIN
        IF NEW."product_url" IS NOT NULL
            AND NEW."product_name" IS NOT NULL
            AND NEW."product_energy" IS NOT NULL
            AND NEW."product_protein" IS NOT NULL
            AND NEW."product_fat" IS NOT NULL
            AND NEW."product_carbs" IS NOT NULL
            AND NEW."product_ingredients" IS NOT NULL
        THEN
            NEW."completed" = 'true';
        END IF;
        RETURN NEW;
    END;
$mark_incomplete_as_completed$ LANGUAGE plpgsql;

-- Create a trigger to check completeness and mark "completed" as true
-- BEFORE inser/update, so that both operations are executed at the same time
CREATE OR REPLACE TRIGGER "check_completeness"
BEFORE INSERT OR UPDATE ON "incomplete_products"
FOR EACH ROW
EXECUTE FUNCTION mark_incomplete_as_completed();

-- incomplete_prices
CREATE TABLE "incomplete_prices" (
    "id" SERIAL PRIMARY KEY,
    "author_id" INT NOT NULL REFERENCES "users", -- user who inserted the data
    "product_id" INT NOT NULL REFERENCES "products",
    -- WARNING references an incomplete product or a complete product!!! ???????
    "store_id" INT REFERENCES "stores",
    -- WARNING references an incomplete store or a complete store!!! ???????
    "store_name" VARCHAR(64) NOT NULL,
    "store_website" VARCHAR(2048),
    "store_address" VARCHAR(2048),
    -- "long_lat" geography(point), -- longitude first then latitude, example: 'POINT(-118.4079 33.9434)'
    -- To use it, you must first install the PostGIS extension and then create a table with a geography(point) column, using functions like ST_GeogFromText to insert data
    "country_id" INT REFERENCES "countries",
    "price_date" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "product_price" SMALLINT NOT NULL CHECK ("product_price" >= 0), -- in cents per packaging
    "product_weight" INT CHECK ("product_weight" >= 0), -- packaging size in grams
    -- Weight OR quantity
    "product_quantity" INT CHECK ("product_quantity" >= 0), -- packaging size in units
    -- "product_pic_file" bytea, -- https://www.postgresql.org/docs/7.4/jdbc-binary-data.html
    -- "product_pic_url" VARCHAR(2048) DEFAULT 'https://pix.org/no_pic.png', -- https://prices.openfoodfacts.org/api/docs
    "currency_id" SMALLINT NOT NULL REFERENCES "currencies",
    "comment" VARCHAR(2048),
    "completed" BOOLEAN NOT NULL DEFAULT 'false'
);

