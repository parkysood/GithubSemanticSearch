import psycopg2
import qdrant_client
from qdrant_client.http.models import PointStruct
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# PostgreSQL connection
conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    dbname=os.getenv("PG_DB_NAME"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PWD"),
    port=os.getenv("PG_PORT"),
)
conn.autocommit = True
cursor = conn.cursor()

# Safe table creation
cursor.execute("""
    CREATE TABLE IF NOT EXISTS repositories (
        url TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        language TEXT,
        owner TEXT,
        license TEXT,
        stars INT,
        updated_at TIMESTAMP
    )
""")

# Qdrant Client
qdrant = qdrant_client.QdrantClient(
    url=os.getenv("QD_URL"),
    # api_key=os.getenv("QD_API_KEY"),  # TODO: Only needed for cloud hosting, not local
)


# Load data and embeddings into data storages
def load_data(repos):
    for repo in repos:
        # No need to sanitize since user is not inputting here (data coming from GitHub API)
        values = (
            repo["url"],
            repo["name"],
            repo["description"],
            repo["language"],
            repo["owner"],
            repo["license"],
            int(repo["stars"]),
            repo["updated_at"],
        )

        # Upsert into Postgres DB. Use santization here (loading user-generated data)
        cursor.execute(
            """
            INSERT INTO repositories (url, name, description, language, owner, license, stars, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE SET
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                language = EXCLUDED.language,
                owner = EXCLUDED.owner,
                license = EXCLUDED.license,
                stars = EXCLUDED.stars,
                updated_at = EXCLUDED.updated_at;
        """,
            values,
        )

        # Upsert into Qdrant
        if repo.get("embedding"):
            point = PointStruct(
                id=repo["url"],
                vector=repo["embedding"],
                payload={
                    "name": repo["name"],
                    "description": repo["description"],
                    "language": repo["language"],
                    "url": repo["url"],
                },
            )

            # TODO: FIX COLLECTION NAME
            qdrant.upsert(collection_name="", points=[point])
