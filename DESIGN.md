# Design Document

By Noémie Baudouin

Video overview: [Students Kitchen](https://youtu.be/E-9U2HkT-IU)


## Scope

This database named `students_kitchen.db` is aimed at solving a problem that nearly everyone is facing in our modern lives: eating cheap and fast, while caring about health.
`students_kitchen.db` will allow its users to feed the platform with recipes, and collect all the data necessary to provide a ranking of the recipes based on various parameters:
- economical cost
- time cost
- nutrition facts

As an example, the provided SQL VIEW included in `schema.sql` already permits to catch a glimpse of what kind of rankings we could extract from `students_kitchen.db`. I am already beginning a python project to display calculated tables based on the efficiency of recipes.

The scope of `students_kitchen.db` includes any person as a potential user, any recipe, any ingredient, any ingredient provider.
The scope of `students_kitchen.db` doesn't yet include any restaurant or processed food company, but I will include them as soon as possible, in order to also rank their recipes.


## Functional Requirements

Users can CRUD the following tables:
- `"users"` first and foremost
- `"recipes"` to explain their best cooking tricks
- `"ingredients"` to make them available for their `"recipes"` and `JOIN "grams" ON "recipes"`
- `"grams"` to add the quantity of each ingredient to their recipe
- `"prices"` for each ingredient
- `"providers"` for the source of each price


## Representation

Entities are captured in SQLite tables with the following schema:


### Entities

The database includes the following entities:


#### Users

The `users` table includes:

* `id`, which specifies the unique ID for the user as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `username`, which specifies the user's username as `TEXT`, given `TEXT` is appropriate for name fields. A `UNIQUE` constraint ensures no two students have the same username.
* `email`, which specifies the email associated with the username. `TEXT` is appropriate for email fields.
* `password`, which specifies the password associated with the username. `TEXT` is used for the same reason as `username`.
* `avatar`, which gives the option to upload a small image file. `BLOB` is used to store data files up to 1GB, largely sufficient for an avatar picture.
* `contributions`, which is the number of contributions to the database a user has achieved, as an `INTEGER`. This number will be shown in their profile to encourage contributions.

`avatar` and `contributions` are not required, hence these two columns do not have the `NOT NULL` constraint applied.


#### Recipes

The `recipes` table includes:

* `id`, which specifies the unique ID for the recipe as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `name`, which specifies the recipe's name as `TEXT`, given `TEXT` is appropriate for name fields. There can be various recipes with the same name.
* `author_id`, which is the ID of the user who submitted the recipe, as an `INTEGER`. This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `users` table to ensure data integrity.
* `duration`, which is the number of minutes a recipe might take to prepare, as an `INTEGER`.
* `description`, which describes the steps to prepare the recipe as `TEXT`, given that `TEXT` can store long-form text. A `UNIQUE` constraint ensures descriptions have to differ, even if two recipes have the same name.

All columns are required and hence have the `NOT NULL` constraint applied.


#### Available ingredients

The `ingredients` table includes:

* `id`, which specifies the unique ID for the ingredient as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `name`, which specifies the ingredient's name as `TEXT`, given `TEXT` is appropriate for name fields. A `UNIQUE` constraint ensures names have to differ.
* `protein`, which specifies the ingredient's protein rate per 100g as an `INTEGER`.
* `carbs`, which specifies the ingredient's carbs rate per 100g as an `INTEGER`.
* `fat`, which specifies the ingredient's fat rate per 100g as an `INTEGER`.

All columns are required and hence have the `NOT NULL` constraint applied.


#### Ingredients for each recipe in grams per person

The `grams` table includes:

* `recipe_id`, which is the ID of the related recipe as an `INTEGER`. This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `recipes` table to ensure data integrity.
* `ingredient_id`, which is the ID of the related ingredient as an `INTEGER`. This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `ingredients` table to ensure data integrity.
* `grams_per_person`, which specifies the ingredient's quantity per person as an `INTEGER`.

All columns are required and hence have the `NOT NULL` constraint applied.


#### Providers of ingredients

The `providers` table includes:

* `id`, which specifies the unique ID for the provider of ingredients as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `name`, which specifies the recipe's name as `TEXT`, given `TEXT` is appropriate for name fields. There can be various providers with the same name.
* `address`, which specifies the provider's address as `TEXT`, given `TEXT` is appropriate for address fields. A `UNIQUE` constraint ensures addresses have to differ, even if two providers have the same name.
* `website`, which specifies the provider's website URL as `TEXT`, given `TEXT` is appropriate for URL fields. A `UNIQUE` constraint ensures websites have to differ, even if two providers have the same name.

Only the `name` column is required and hence has the `NOT NULL` constraint applied.


#### Prices of each ingredient

The `prices` table includes:

* `id`, which specifies the unique ID for the listed price, as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `ingredient_id`, which is the ID of the related priced ingredient as an `INTEGER`. This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `ingredients` table to ensure data integrity.
* `provider_id`, which is the ID of the related ingredient provider as an `INTEGER`. This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `providers` table to ensure data integrity. It is not required in case some ingredient can be bought on a open market.
* `date`, which specifies when the price has been listed. Timestamps in SQLite can be conveniently stored as `NUMERIC`, per SQLite documentation at <https://www.sqlite.org/datatype3.html>. The default value for the `date` attribute is the current timestamp, as denoted by `DEFAULT CURRENT_TIMESTAMP`.
* `price`, which specifies the listed ingredient's price in cents per 100g as an `INTEGER`. There can be various prices according to various dates.
* `currency`, which allows to chose between different `TEXT` options, with the help of a `CHECK("currency" IN ('Euro', 'USD', 'Pound', 'Yen'))` constraint.
* `author_id`, which is the ID of the user who submitted the price, as an `INTEGER`. This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `users` table to ensure data integrity.
* `comment`, which lets the user add a comment as `TEXT`, given that `TEXT` can store long-form text.

All columns but `provider_id` an `comment` are required and hence have the `NOT NULL` constraint applied.


#### a VIEW of the economical cost, time cost, protein and fat of a recipe

The `cost_time_protein_fat` VIEW is used to represent the most effective recipes to eat healthy when you lack time and money, by joining the columns `"recipes"."name"`, `"recipes"."duration"`, `"ingredients"."name"`, `"grams"."grams_per_person"`, `"ingredients"."protein"`, "`ingredients"."fat"`, and `"prices"."price"` altogether.



### Relationships

The below entity relationship diagram describes the relationships among the entities in the database.


    USERS ||--o{ RECIPES
    USERS ||--o{ PRICES
    RECIPES ||--|{ GRAMS
    GRAMS ||--|| INGREDIENTS
    INGREDIENTS ||--|{ PRICES
    PRICES ||--|| PROVIDERS


[![ER Diagram](https://mermaid.ink/img/pako:eNptkc1uwjAQhF_F2nNAYEx-fKsgQjlAUWh7qHJx8QKREhs5jlqa8O7FSRr10L3t-JvZlbeBo5YIHNCsc3E2oswUedTrIU4PpG0nE92QNF4l-_hAOPk02uI_xD5NVh1Q5JVF2RO_Nse0DdmkT1uHHLWyIldVD_Vqh7Qk2W3SeJ3EuxcH6lOP_FWHrHHeUVd2SBq0IWqfPr8la7ciJxlUupDk45ZBphwMHpxNLoGfRFGhByWaUrgeGvecgb1giRk4q8STqAvrrPeH7yrUu9YlcGvqh9Po-nwZc-qrFBaHjxxVg0qiWelaWeBzGsy7FOANfAFny8V0Rv2IRgEN2ZxGzIMbcDqb-mHAWMRYuFjSwPfvHnx3g2fTMFh6gDK32mz763VHvP8A6sqKkA?type=png)](https://mermaid.live/edit#pako:eNptkc1uwjAQhF_F2nNAYEx-fKsgQjlAUWh7qHJx8QKREhs5jlqa8O7FSRr10L3t-JvZlbeBo5YIHNCsc3E2oswUedTrIU4PpG0nE92QNF4l-_hAOPk02uI_xD5NVh1Q5JVF2RO_Nse0DdmkT1uHHLWyIldVD_Vqh7Qk2W3SeJ3EuxcH6lOP_FWHrHHeUVd2SBq0IWqfPr8la7ciJxlUupDk45ZBphwMHpxNLoGfRFGhByWaUrgeGvecgb1giRk4q8STqAvrrPeH7yrUu9YlcGvqh9Po-nwZc-qrFBaHjxxVg0qiWelaWeBzGsy7FOANfAFny8V0Rv2IRgEN2ZxGzIMbcDqb-mHAWMRYuFjSwPfvHnx3g2fTMFh6gDK32mz763VHvP8A6sqKkA)

As detailed by the diagram:

* One user is capable of uploading 0 to many contributions. 0, if they have yet to submit any contribution, and many if they submit to more than one recipe or price listing. A contribution is made by one and only one user.
* A recipe is associated with one or more quantity of ingredients, in grams. At the same time, an ingredient can appear in 0 to many recipes, recipes and ingredients always being related with a quantity in grams.
* A price is associated with one and only one user, with one and only one provider, and with one and only one ingredient, whereas a user can have listed 0 to many prices, and an ingredient also can have one to many prices, according to the provider.


## Optimizations

The most demanded data will obviously be the ingredients name, we can think for example about an ingredient like "wheat".
For that reason, an index is created on the `"name"` column to speed the identification of `"ingredients"`.


## Limitations

As for now, the schema only allows user-made recipes, while I am planning to allow providers to post their own recipes of the processed food they sell, so that visitors can compare health/time/cost recipes between home-made and ready-made options too.