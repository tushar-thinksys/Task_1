import asyncio
from app.db.session import engine
from app.api.v1.auth.model import User, OTP  # Import all models
from app.db.base import Base

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_models())
