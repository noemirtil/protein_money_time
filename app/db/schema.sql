-- \l   -- List databases
-- \dt  -- List tables
-- \du  -- List users
-- DROP TABLE IF EXISTS "products";
-- DROP TABLE IF EXISTS "brands";
-- DROP TABLE IF EXISTS "stores";
-- DROP TABLE IF EXISTS "prices";
-- DROP TABLE IF EXISTS "currencies";

-- Represent every user registered in the platform
-- Count the number of its contributions to show in their profile
DROP TABLE IF EXISTS "users";
CREATE TABLE "users" (
    "id" SERIAL,
    "username" VARCHAR(32) NOT NULL UNIQUE,
    "email" VARCHAR(320) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    -- "avatar" BLOB,
    "contributions" INTEGER,
    PRIMARY KEY("id")
);