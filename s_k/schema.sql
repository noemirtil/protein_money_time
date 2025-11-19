-- DROP TABLE IF EXISTS "users";
-- DROP TABLE IF EXISTS "recipes";
-- DROP TABLE IF EXISTS "ingredients";
-- DROP TABLE IF EXISTS "grams";
-- DROP TABLE IF EXISTS "providers";
-- DROP TABLE IF EXISTS "prices";
-- DROP VIEW IF EXISTS "cost_time_protein_fat";










--          CS50 final project by Noémie Baudouin

--          Project's name: "Students kitchen"
--          https://github.com/noemirtil/
--          edX username: 2508_4BEG
--          Barcelona, Spain - Saturday, November 8, 2025














-- Represent every user registered in the platform
-- Count the number of its contributions to show in their profile
CREATE TABLE "users" (
    "id" INTEGER,
    "username" TEXT NOT NULL UNIQUE,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "avatar" BLOB,
    "contributions" INTEGER,
    PRIMARY KEY("id")
);

-- Represent every recipe uploaded by users
-- There can be various recipes with the same name, but their descriptions have to differ
CREATE TABLE "recipes" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "author_id" INTEGER NOT NULL,
    "duration" INTEGER NOT NULL,
    "description" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id"),
    FOREIGN KEY("author_id") REFERENCES "users"("id")
);

-- Represent any ingredient available on earth, with nutriments per 100g in order to calculate for each recipe
CREATE TABLE "ingredients" (
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    "protein" INTEGER NOT NULL,
    "carbs" INTEGER NOT NULL,
    "fat" INTEGER NOT NULL,
    PRIMARY KEY("id")
);

-- Represent the quantity of each ingredient for each recipe
-- No need for a primary key
CREATE TABLE "grams" (
    "recipe_id" INTEGER NOT NULL,
    "ingredient_id" INTEGER NOT NULL,
    "grams_per_person" INTEGER NOT NULL,
    FOREIGN KEY("recipe_id") REFERENCES "recipes"("id"),
    FOREIGN KEY("ingredient_id") REFERENCES "ingredients"("id")
);

-- Represent the providers of ingredients
CREATE TABLE "providers" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "address" TEXT UNIQUE,
    "website" TEXT UNIQUE,
    PRIMARY KEY("id")
);

-- Represent the prices in cents per 100g seen for each ingredient and their corresponding suppliers
-- There can be various prices according to various dates
CREATE TABLE "prices" (
    "id" INTEGER,
    "ingredient_id" INTEGER NOT NULL,
    "provider_id" INTEGER,
    "date" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "price" INTEGER NOT NULL,
    "currency" TEXT NOT NULL CHECK("currency" IN ('Euro', 'USD', 'Pound', 'Yen')),
    "author_id" INTEGER NOT NULL,
    "comment" TEXT,
    PRIMARY KEY("id"),
    FOREIGN KEY("ingredient_id") REFERENCES "ingredients"("id"),
    FOREIGN KEY("provider_id") REFERENCES "providers"("id"),
    FOREIGN KEY("author_id") REFERENCES "users"("id")
);

-- Represent the most effective recipes to eat healthy when you lack time and money
CREATE VIEW "cost_time_protein_fat" AS
SELECT "recipes"."name" AS "recipe", "recipes"."duration", "ingredients"."name" AS "ingredient", "grams"."grams_per_person", "ingredients"."protein", "ingredients"."fat", "prices"."price" FROM "recipes"
JOIN "grams" ON "grams"."recipe_id" = "recipes"."id"
JOIN "ingredients" ON "grams"."ingredient_id" = "ingredients"."id"
JOIN "prices" ON "prices"."ingredient_id" = "ingredients"."id";

-- Create indexes to speed common searches
CREATE INDEX "ingredient_search" ON "ingredients" ("name");