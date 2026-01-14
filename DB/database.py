from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .core import Base

# Configuración para PostgreSQL
DATABASE_URL = "postgresql+asyncpg://jera:105181@localhost:5432/powerview"

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True,
    pool_size=10,  # Número de conexiones en el pool
    max_overflow=5,  # Conexiones adicionales cuando el pool está lleno
    connect_args={
       "server_settings": {
            "application_name": "PowerView",
            "statement_timeout": "30000",  # 30 segundos timeout por consulta
        },
        "command_timeout": 30  # Timeout para conexión inicial
    }
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False  
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


