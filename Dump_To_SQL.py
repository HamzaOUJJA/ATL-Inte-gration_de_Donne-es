import pandas as pd
from sqlalchemy import create_engine

# Database connection settings
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "movies_db"

# Create database connection
db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)

# Load cleaned CSVs
df_movies = pd.read_csv("cleaned_movies.csv")
df_genres = pd.read_csv("cleaned_genres.csv")

# Create tables if not exists
with engine.connect() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            title TEXT,
            year TEXT,
            rating FLOAT,
            votes INT,
            runtime INT,
            director TEXT
        );

        CREATE TABLE IF NOT EXISTS genres (
            id SERIAL PRIMARY KEY,
            movie_id INT REFERENCES movies(id),
            genre TEXT
        );
    """)

# Load movies data
df_movies.to_sql("movies", engine, if_exists="append", index=False)

# Load genres data (linking to movies)
with engine.connect() as conn:
    for _, row in df_genres.iterrows():
        result = conn.execute(f"SELECT id FROM movies WHERE title = '{row['MOVIES']}'").fetchone()
        if result:
            movie_id = result[0]
            conn.execute(f"INSERT INTO genres (movie_id, genre) VALUES ({movie_id}, '{row['GENRE']}')")
    
print("Data successfully inserted into PostgreSQL.")
