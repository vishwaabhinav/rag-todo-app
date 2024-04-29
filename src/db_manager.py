import aiosqlite

DATABASE_URL = "sqlite:///./text_chunks.db"

async def initialize_db():
    """Initialize the database and create necessary tables."""
    async with aiosqlite.connect("text_chunks.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL
            )
        """)
        await db.commit()

async def store_chunk(id_, text):
    """Store a text chunk in the database."""
    async with aiosqlite.connect("text_chunks.db") as db:
        await db.execute("INSERT OR REPLACE INTO chunks (id, text) VALUES (?, ?)", (id_, text))
        await db.commit()

async def get_chunk(id_):
    """Retrieve a text chunk from the database based on its ID."""
    async with aiosqlite.connect("text_chunks.db") as db:
        cursor = await db.execute("SELECT text FROM chunks WHERE id = ?", (id_,))
        row = await cursor.fetchone()
        return row[0] if row else None
