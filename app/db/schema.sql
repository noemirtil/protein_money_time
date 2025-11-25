-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS "prices" CASCADE;
DROP TABLE IF EXISTS "stores" CASCADE;
DROP TABLE IF EXISTS "junction_currency_country" CASCADE;
DROP TABLE IF EXISTS "products" CASCADE;
DROP TABLE IF EXISTS "countries" CASCADE;
DROP TABLE IF EXISTS "currencies" CASCADE;
DROP TABLE IF EXISTS "brands" CASCADE;
DROP TABLE IF EXISTS "users" CASCADE;

-- Users table
CREATE TABLE "users" (
    "id" SERIAL PRIMARY KEY,
    "username" VARCHAR(32) NOT NULL UNIQUE,
    "email" VARCHAR(320) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "contributions" INT DEFAULT 0
    -- Removed "deleted" for now - add later if needed
);

-- Brands table
CREATE TABLE "brands" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL UNIQUE,
    "website" VARCHAR(2048) NOT NULL UNIQUE,
    "inactive" BOOLEAN NOT NULL DEFAULT false
);

-- Fixed trigger function
CREATE OR REPLACE FUNCTION discontinue_product()
RETURNS TRIGGER AS $$
    BEGIN
        UPDATE "products" 
        SET "discontinued" = true 
        WHERE "brand_id" = NEW."id";
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

-- Fixed trigger
CREATE OR REPLACE TRIGGER "inactive_brand"
AFTER UPDATE OF "inactive" ON "brands"
FOR EACH ROW
WHEN (NEW."inactive" = true)
EXECUTE FUNCTION discontinue_product();

-- Products table
CREATE TABLE "products" (
    "id" SERIAL PRIMARY KEY,
    "off_code" BIGINT UNIQUE,
    "url" VARCHAR(2048) NOT NULL UNIQUE,
    "name" VARCHAR(320) NOT NULL,
    "brand_id" INT REFERENCES "brands",
    "ingredients_text" TEXT NOT NULL,
    "energy" SMALLINT NOT NULL CHECK ("energy" BETWEEN 0 AND 5000),
    "fat" REAL NOT NULL CHECK ("fat" BETWEEN 0 AND 100),
    "sat_fat" REAL CHECK ("sat_fat" BETWEEN 0 AND 100),
    "carbs" REAL NOT NULL CHECK ("carbs" BETWEEN 0 AND 100),
    "sugars" REAL CHECK ("sugars" BETWEEN 0 AND 100),
    "fiber" REAL CHECK ("fiber" BETWEEN 0 AND 100),
    "protein" REAL NOT NULL CHECK ("protein" BETWEEN 0 AND 100),
    "sodium" REAL CHECK ("sodium" BETWEEN 0 AND 100),
    "c_vitamin" REAL CHECK ("c_vitamin" BETWEEN 0 AND 100),
    "nutr_score_fr" SMALLINT CHECK ("nutr_score_fr" BETWEEN -20 AND 50),
    "discontinued" BOOLEAN NOT NULL DEFAULT false
);

-- Currencies table
CREATE TABLE "currencies" (
    "id" SMALLSERIAL PRIMARY KEY,
    "currency_name" VARCHAR(42) NOT NULL UNIQUE,
    "currency_code" VARCHAR(3) NOT NULL UNIQUE
);

-- Countries table
CREATE TABLE "countries" (
    "id" SMALLSERIAL PRIMARY KEY,
    "country" VARCHAR(60) NOT NULL UNIQUE
);

-- Junction table
CREATE TABLE "junction_currency_country" (
    "id" SMALLSERIAL PRIMARY KEY,
    "country_id" SMALLINT REFERENCES "countries",
    "currency_id" SMALLINT REFERENCES "currencies"
);

-- Stores table
CREATE TABLE "stores" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "address" VARCHAR(2048) UNIQUE,
    "country_id" INT REFERENCES "countries",
    "website" VARCHAR(2048) UNIQUE,
    "inactive" BOOLEAN NOT NULL DEFAULT false
);

-- Prices table
CREATE TABLE "prices" (
    "id" BIGSERIAL PRIMARY KEY,
    "product_id" INT NOT NULL REFERENCES "products",
    "store_id" INT NOT NULL REFERENCES "stores",
    "date" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "price" SMALLINT NOT NULL CHECK ("price" >= 0),
    "weight" INT CHECK ("weight" >= 0),
    "quantity" INT CHECK ("quantity" >= 0),
    "currency_id" SMALLINT NOT NULL REFERENCES "currencies",
    "author_id" INT NOT NULL REFERENCES "users",
    "comment" VARCHAR(2048),
    "deleted" BOOLEAN NOT NULL DEFAULT false
);