-- Select Euro countries
SELECT "country", "currency_name" FROM "countries"
JOIN "junction_currency_country" ON "junction_currency_country"."country_id" = "countries"."id"
JOIN "currencies" ON "junction_currency_country"."currency_id" = "currencies"."id"
WHERE "currency_code" = 'EUR';

-- Select products with brand names
SELECT "products"."off_code", "products"."name", "brands"."name", "brands"."website" FROM "products"
JOIN "brands" ON "brands"."id" = "products"."brand_id";


-- INSERT INTO "recipes" ("name", "duration", "description", "author_id")
-- VALUES ('Lentils and eggs', '15', 'Boil the lentils, add the eggs', '1'),
-- ('Spaghetti with mozzarella', '20', 'Boil the spaghettis, add the cheese', '1');

-- INSERT INTO "ingredients" ("name", "protein", "carbs", "fat")
-- VALUES ('Lentils', '9', '31', '1'), ('Eggs', '13', '1', '9'),
-- ('Spaghettis', '6', '30', '1'), ('Mozzarella', '18', '2', '18');

-- INSERT INTO "grams" ("recipe_id", "ingredient_id", "grams_per_person")
-- VALUES ('1', '1', '100'), ('1', '2', '250'), ('2', '3', '100'), ('2', '4', '50');

-- INSERT INTO "prices" ("ingredient_id", "price", "currency", "author_id")
-- VALUES ('1', '35', 'Euro', '1'), ('2', '43', 'Euro', '1'),
-- ('3', '16', 'Euro', '1'), ('4', '112', 'Euro', '1');

-- -- To find the price of the lentils:
-- SELECT "ingredients"."name" AS "ingredient",
-- "prices"."price", "providers"."name" AS "provider"
-- FROM "ingredients"
-- JOIN "prices" ON "prices"."ingredient_id" = "ingredients"."id"
-- JOIN "providers" ON "prices"."provider_id" = "providers"."id"
-- WHERE "ingredient" LIKE '%lentil%';

-- -- To look for a cost-effective recipe
-- SELECT "recipe",
-- SUM("grams_per_person" * "price") AS 'cost',
-- SUM("protein" * "grams_per_person") AS 'protein',
-- SUM("fat" * "grams_per_person") AS 'fat',
-- "duration"
-- FROM "cost_time_protein_fat"
-- GROUP BY "recipe"
-- ORDER BY "cost", "protein" DESC, "fat", "duration";

