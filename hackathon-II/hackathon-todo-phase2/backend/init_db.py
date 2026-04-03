"""
Database initialization script for the Todo Application.

This script creates all necessary tables and indexes for the application.
"""
import asyncio
from sqlmodel import SQLModel
from models import User, Task
from db import engine


def create_db_and_tables():
    """
    Creates all database tables based on SQLModel definitions.
    """
    print("Creating database tables...")

    # Create all tables
    SQLModel.metadata.create_all(engine)

    print("Database tables created successfully!")
    print("- Users table")
    print("- Tasks table")
    print("- Indexes: tasks.user_id, tasks.completed, tasks.created_at")


if __name__ == "__main__":
    create_db_and_tables()