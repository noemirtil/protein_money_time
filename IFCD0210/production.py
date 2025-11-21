import os

DATABASE_URI = "postgresql+psycopg://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
    dbuser=os.getenv("postgresadmin"),
    dbpass=os.getenv(
        "@Microsoft.KeyVault(SecretUri=https://pmtks5rqp3cc57aa-vault.vault.azure.net/secrets/azure-postgresql-password-b896d/5984c1dc23a54e4ba1be1107f3deb2a9)"
    ),
    dbhost=os.getenv("p-m-t-ks5rqp3cc57aa-server.postgres.database.azure.com"),
    dbname=os.getenv("p-m-t-ks5rqp3cc57aa-database"),
)
