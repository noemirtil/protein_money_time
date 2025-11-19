\l
\dt
\du

-- DROP TABLE IF EXISTS "users";
-- DROP TABLE IF EXISTS "products";
-- DROP TABLE IF EXISTS "brands";
-- DROP TABLE IF EXISTS "stores";
-- DROP TABLE IF EXISTS "prices";
-- DROP TABLE IF EXISTS "currencies";

-- Represent every user registered in the platform
-- Count the number of its contributions to show in their profile
CREATE TABLE "users" (
    "id" SERIAL,
    "username" VARCHAR(32) NOT NULL UNIQUE,
    "email" VARCHAR(320) NOT NULL,
    "password" VARCHAR(64) NOT NULL,
    -- "avatar" BLOB,
    "contributions" INTEGER,
    PRIMARY KEY("id")
);

-- Represent any product (ingredient or ready-made), with nutriments
-- /opt/homebrew/bin/createuser per 100g in order to calculate for each recipe
CREATE TABLE "products" (
    "id" SERIAL,
    "off_code" BIGINT UNIQUE, -- Open Food Facts database code
    "url" VARCHAR(2048) NOT NULL UNIQUE,
    "name" VARCHAR(320) NOT NULL UNIQUE,
    "brand_id" INTEGER, -- can be null if it is a simple ingredient
    "ingredients_text" TEXT NOT NULL, -- can be only one ingredient if it is a simple ingredient
    "energy" SMALLINT NOT NULL, -- for 100g
    "fat" SMALLINT NOT NULL, -- for 100g
    "sat_fat" REAL, -- for 100g
    "carbs" REAL NOT NULL, -- for 100g
    "sugars" REAL, -- for 100g
    "protein" REAL NOT NULL, -- for 100g
    "fiber" REAL, -- for 100g
    "sodium" REAL, -- for 100g
    "c_vitamin" REAL, -- for 100g
    "nutr_score_uk " SMALLINT, -- for 100g
    PRIMARY KEY("id"),
    FOREIGN KEY("brand_id") REFERENCES "brands"("id")
);

-- Represent the brands which make the products
CREATE TABLE "brands" (
    "id" SERIAL,
    "name" VARCHAR(64) NOT NULL UNIQUE,
    "website" VARCHAR(2048) NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

-- Represent the stores where the prices were seen
CREATE TABLE "stores" (
    "id" SERIAL,
    "name" VARCHAR(64) NOT NULL UNIQUE,
    "address" VARCHAR(100) UNIQUE, -- can be null for online stores
    "country" VARCHAR(58), -- can be null for online stores
    "website" VARCHAR(2048) UNIQUE, -- can be null for physical stores
    PRIMARY KEY("id"),
    FOREIGN KEY("country") REFERENCES "currencies"("id")
);

-- Represent the prices in cents per 100g seen for each product and their corresponding stores
-- There can be various prices according to various dates, various stores, various packaging sizes
CREATE TABLE "prices" (
    "id" BIGSERIAL,
    "product_id" INTEGER NOT NULL,
    "store_id" INTEGER,
    "date" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "price" SMALLINT NOT NULL, -- in cents per 100g
    "weight" INTEGER, -- packaging size in grams
    "quantity" INTEGER, -- packaging size in units
    "currency_id" SMALLINT NOT NULL,
    "author_id" INTEGER NOT NULL, -- user who uploaded the data
    "comment" TEXT,
    PRIMARY KEY("id"),
    FOREIGN KEY("product_id") REFERENCES "products"("id"),
    FOREIGN KEY("store_id") REFERENCES "stores"("id"),
    FOREIGN KEY("author_id") REFERENCES "users"("id"),
    FOREIGN KEY("currency_id") REFERENCES "currencies"("id")
);

CREATE TABLE "currencies" (
    -- https://en.wikipedia.org/wiki/ISO_4217#List_of_ISO_4217_currency_codes
    "id" SMALLINT,
    "country" VARCHAR(58) NOT NULL UNIQUE,
    "currency" VARCHAR(3) NOT NULL, -- currency code
    PRIMARY KEY "id"
)


-- DROP TABLE IF EXISTS "recipes";
-- DROP TABLE IF EXISTS "grams";
-- DROP VIEW IF EXISTS "cost_time_protein_fat";

-- -- Represent every recipe uploaded by users
-- -- There can be various recipes with the same name, but their descriptions have to differ
-- CREATE TABLE "recipes" (
--     "id" INTEGER,
--     "name" TEXT NOT NULL,
--     "author_id" INTEGER NOT NULL,
--     "duration" INTEGER NOT NULL,
--     "description" TEXT NOT NULL UNIQUE,
--     PRIMARY KEY("id"),
--     FOREIGN KEY("author_id") REFERENCES "users"("id")
-- );

-- -- Represent the quantity of each ingredient for each recipe
-- -- No need for a primary key
-- CREATE TABLE "grams" (
--     "recipe_id" INTEGER NOT NULL,
--     "ingredient_id" INTEGER NOT NULL,
--     "grams_per_person" INTEGER NOT NULL,
--     FOREIGN KEY("recipe_id") REFERENCES "recipes"("id"),
--     FOREIGN KEY("ingredient_id") REFERENCES "ingredients"("id")
-- );


    -- -- Represent the most effective recipes to eat healthy when you lack time and money
    -- CREATE VIEW "cost_time_protein_fat" AS
    -- SELECT "recipes"."name" AS "recipe", "recipes"."duration", "ingredients"."name" AS "ingredient", "grams"."grams_per_person", "ingredients"."protein", "ingredients"."fat", "prices"."price" FROM "recipes"
    -- JOIN "grams" ON "grams"."recipe_id" = "recipes"."id"
    -- JOIN "ingredients" ON "grams"."ingredient_id" = "ingredients"."id"
    -- JOIN "prices" ON "prices"."ingredient_id" = "ingredients"."id";

    -- -- Create indexes to speed common searches
    -- CREATE INDEX "ingredient_search" ON "ingredients" ("name");