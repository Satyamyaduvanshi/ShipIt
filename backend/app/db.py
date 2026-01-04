from prisma import Prisma

# Global Database Instance
db = Prisma()

def connect_db():
    """Connect to the database if not already connected."""
    if not db.is_connected():
        db.connect()
        print("✅ Connected to Neon DB!")

def disconnect_db():
    """Disconnect from the database."""
    if db.is_connected():
        db.disconnect()
        print("🛑 Disconnected from Neon DB.")