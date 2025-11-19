-- Test data seeding
INSERT INTO "users" ("username", "email", "password") VALUES ('Noemi', "noemi@gmail.com", 'password');

INSERT INTO "recipes" ("name", "duration", "description", "author_id")
VALUES ('Lentils and eggs', '15', 'Boil the lentils, add the eggs', '1'),
('Spaghetti with mozzarella', '20', 'Boil the spaghettis, add the cheese', '1');

INSERT INTO "ingredients" ("name", "protein", "carbs", "fat")
VALUES ('Lentils', '9', '31', '1'), ('Eggs', '13', '1', '9'),
('Spaghettis', '6', '30', '1'), ('Mozzarella', '18', '2', '18');

INSERT INTO "grams" ("recipe_id", "ingredient_id", "grams_per_person")
VALUES ('1', '1', '100'), ('1', '2', '250'), ('2', '3', '100'), ('2', '4', '50');

INSERT INTO "providers" ("name", "website") VALUES ('Carrefour', 'https://www.carrefour.es/');

INSERT INTO "prices" ("ingredient_id", "price", "currency", "author_id")
VALUES ('1', '35', 'Euro', '1'), ('2', '43', 'Euro', '1'),
('3', '16', 'Euro', '1'), ('4', '112', 'Euro', '1');

-- Test data updating
UPDATE "grams" SET "grams_per_person" = '250' WHERE "recipe_id" = '2' AND "ingredient_id" = '3';
UPDATE "grams" SET "grams_per_person" = '100' WHERE "recipe_id" = '2' AND "ingredient_id" = '4';
UPDATE "prices" SET "provider_id" = '1' WHERE "id" IN ('1', '2', '3', '4');

-- To find the price of the lentils:
SELECT "ingredients"."name" AS "ingredient",
"prices"."price", "providers"."name" AS "provider"
FROM "ingredients"
JOIN "prices" ON "prices"."ingredient_id" = "ingredients"."id"
JOIN "providers" ON "prices"."provider_id" = "providers"."id"
WHERE "ingredient" LIKE '%lentil%';

-- To look for a cost-effective recipe
SELECT "recipe",
SUM("grams_per_person" * "price") AS 'cost',
SUM("protein" * "grams_per_person") AS 'protein',
SUM("fat" * "grams_per_person") AS 'fat',
"duration"
FROM "cost_time_protein_fat"
GROUP BY "recipe"
ORDER BY "cost", "protein" DESC, "fat", "duration";

-- Test user deleting
DELETE FROM "users" WHERE "username" = 'Noemi';
