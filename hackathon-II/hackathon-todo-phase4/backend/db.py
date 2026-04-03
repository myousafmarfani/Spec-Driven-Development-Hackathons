from sqlmodel import Session, create_engine
from sqlalchemy import Engine
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the database engine
engine: Engine = create_engine(DATABASE_URL, echo=False)


def get_engine() -> Engine:
    """
    Returns the database engine instance.
    """
    return engine


def get_session() -> Generator[Session, None, None]:
    """
    Yields a database session for use with dependency injection.
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    Creates database tables based on SQLModel models.
    This should be called when initializing the application.
    """
    from sqlmodel import SQLModel
    from models import User, Task
    # Import new models to ensure they're registered with SQLModel
    from src.models.conversation import Conversation
    from src.models.message import Message

    # Import models to ensure they're registered with SQLModel
    SQLModel.metadata.create_all(engine)