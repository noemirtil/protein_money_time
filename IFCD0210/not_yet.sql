

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