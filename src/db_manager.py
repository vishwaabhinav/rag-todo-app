import aiosqlite
import json

DATABASE_URL = "sqlite:///./text_embeddings.db"

async def initialize_db():
    """Initialize the database and create necessary tables."""
    async with aiosqlite.connect("text_embeddings.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS text_embeddings (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                embedding TEXT NOT NULL
            )
        """)
        await db.commit()

async def store_data(id_, text, embedding):
    """Store a text chunk in the database."""
    embedding_str = json.dumps(embedding)  # Convert list to string
    async with aiosqlite.connect("text_embeddings.db") as db:
        await db.execute("INSERT OR REPLACE INTO text_embeddings (id, text, embedding) VALUES (?, ?, ?)", (id_, text, embedding_str))
        await db.commit()

async def get_data(id_):
    """Retrieve a text chunk from the database based on its ID."""
    async with aiosqlite.connect("text_embeddings.db") as db:
        cursor = await db.execute("SELECT text, embedding FROM text_embeddings WHERE id = ?", (id_,))
        row = await cursor.fetchone()
        if row:
            text, embedding_str = row
            embedding = json.loads(embedding_str)  # Convert string back to list
            return {"text": text, "embedding": embedding}
        else:
            return None
