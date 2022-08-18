import databases

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1z3q2w@localhost/recipe_service"
database = databases.Database(SQLALCHEMY_DATABASE_URL)
