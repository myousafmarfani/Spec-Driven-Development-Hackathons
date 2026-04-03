"""
Security tests to verify user data isolation in the task management system.
These tests ensure that users cannot access, modify, or delete other users' tasks.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select, text
import sys
import os

# Add backend to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from main import app
from models import User, Task
from auth import create_access_token
from db import engine
from jose import JWTError, jwt
from datetime import datetime, timedelta

client = TestClient(app)


def create_test_token(user_id: str) -> str:
    """Creates a test token for a given user ID."""
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_key_for_development")
    ALGORITHM = "HS256"

    expire = datetime.utcnow() + timedelta(minutes=60 * 24 * 7)  # 7 days
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def setup_test_data():
    """Set up test users and tasks in the database."""
    user1_id = "test-user-security-1"
    user2_id = "test-user-security-2"

    with Session(engine) as session:
        # Clean up any existing test data
        session.execute(text('DELETE FROM task WHERE user_id IN (:user1_id, :user2_id)'),
                       {"user1_id": user1_id, "user2_id": user2_id})
        session.execute(text('DELETE FROM user WHERE id IN (:user1_id, :user2_id)'),
                       {"user1_id": user1_id, "user2_id": user2_id})

        # Add test users
        user1 = User(id=user1_id, email="security-test1@example.com", name="Security Test User 1", password_hash="hash1")
        session.add(user1)
        user2 = User(id=user2_id, email="security-test2@example.com", name="Security Test User 2", password_hash="hash2")
        session.add(user2)

        # Add test tasks
        task1 = Task(title="User 1 Security Test Task", description="Task for user 1 security test",
                     user_id=user1_id, completed=False)
        session.add(task1)
        task2 = Task(title="User 2 Security Test Task", description="Task for user 2 security test",
                     user_id=user2_id, completed=False)
        session.add(task2)

        session.commit()

        # Get the task IDs
        task1_id = task1.id
        task2_id = task2.id

    return user1_id, user2_id, task1_id, task2_id


def test_users_cannot_access_other_users_tasks():
    """
    Test that users cannot access other users' tasks via API.
    T034: Test that users cannot access other users' tasks via API
    """
    user1_id, user2_id, task1_id, task2_id = setup_test_data()

    # Create tokens for test users
    user1_token = create_test_token(user1_id)
    user2_token = create_test_token(user2_id)

    # Test: User 1 should be able to access their own task
    response = client.get(
        f"/api/{user1_id}/tasks/{task1_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 200, f"User 1 should be able to access their own task, but got: {response.status_code}"
    print(f"PASS: User 1 can access their own task (Status: {response.status_code})")

    # Test: User 1 should NOT be able to access User 2's task
    response = client.get(
        f"/api/{user2_id}/tasks/{task2_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 403, f"User 1 should NOT be able to access User 2's task, but got: {response.status_code}"
    print(f"PASS: User 1 cannot access User 2's task (Status: {response.status_code})")

    # Test: User 2 should be able to access their own task
    response = client.get(
        f"/api/{user2_id}/tasks/{task2_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert response.status_code == 200, f"User 2 should be able to access their own task, but got: {response.status_code}"
    print(f"PASS: User 2 can access their own task (Status: {response.status_code})")

    # Test: User 2 should NOT be able to access User 1's task
    response = client.get(
        f"/api/{user1_id}/tasks/{task1_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert response.status_code == 403, f"User 2 should NOT be able to access User 1's task, but got: {response.status_code}"
    print(f"PASS: User 2 cannot access User 1's task (Status: {response.status_code})")


def test_users_cannot_modify_other_users_tasks():
    """
    Test that users cannot modify other users' tasks.
    T035: Test that users cannot modify other users' tasks
    """
    user1_id, user2_id, task1_id, task2_id = setup_test_data()

    # Create tokens for test users
    user1_token = create_test_token(user1_id)
    user2_token = create_test_token(user2_id)

    # Test: User 1 should be able to modify their own task
    update_data = {
        "title": "Updated User 1 Task",
        "description": "Updated description for user 1"
    }
    response = client.put(
        f"/api/{user1_id}/tasks/{task1_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 200, f"User 1 should be able to modify their own task, but got: {response.status_code}"
    print(f"PASS: User 1 can modify their own task (Status: {response.status_code})")

    # Test: User 2 should NOT be able to modify User 1's task
    response = client.put(
        f"/api/{user1_id}/tasks/{task1_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert response.status_code == 403, f"User 2 should NOT be able to modify User 1's task, but got: {response.status_code}"
    print(f"PASS: User 2 cannot modify User 1's task (Status: {response.status_code})")


def test_users_cannot_delete_other_users_tasks():
    """
    Test that users cannot delete other users' tasks.
    T036: Test that users cannot delete other users' tasks
    """
    user1_id, user2_id, task1_id, task2_id = setup_test_data()

    # Create tokens for test users
    user1_token = create_test_token(user1_id)
    user2_token = create_test_token(user2_id)

    # Test: User 1 should be able to delete their own task
    response = client.delete(
        f"/api/{user1_id}/tasks/{task1_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 200, f"User 1 should be able to delete their own task, but got: {response.status_code}"
    print(f"PASS: User 1 can delete their own task (Status: {response.status_code})")

    # Set up a new task for the next test
    with Session(engine) as session:
        # Clean up and add a new task for the delete test
        session.execute(text('DELETE FROM task WHERE user_id IN (:user1_id, :user2_id)'),
                       {"user1_id": user1_id, "user2_id": user2_id})

        # Add test tasks again
        task1_new = Task(title="New User 1 Delete Test Task", description="Another task for user 1 to delete",
                         user_id=user1_id, completed=False)
        session.add(task1_new)
        session.commit()
        task1_new_id = task1_new.id

    # Test: User 2 should NOT be able to delete User 1's task
    response = client.delete(
        f"/api/{user1_id}/tasks/{task1_new_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert response.status_code == 403, f"User 2 should NOT be able to delete User 1's task, but got: {response.status_code}"
    print(f"PASS: User 2 cannot delete User 1's task (Status: {response.status_code})")


def cleanup_test_data():
    """Clean up test data from the database."""
    user1_id = "test-user-security-1"
    user2_id = "test-user-security-2"

    with Session(engine) as session:
        session.execute(text('DELETE FROM task WHERE user_id IN (:user1_id, :user2_id)'),
                       {"user1_id": user1_id, "user2_id": user2_id})
        session.execute(text('DELETE FROM user WHERE id IN (:user1_id, :user2_id)'),
                       {"user1_id": user1_id, "user2_id": user2_id})
        session.commit()


if __name__ == "__main__":
    try:
        # Run the tests
        test_users_cannot_access_other_users_tasks()
        print("PASS: Test T034 - Users cannot access other users' tasks\n")

        test_users_cannot_modify_other_users_tasks()
        print("PASS: Test T035 - Users cannot modify other users' tasks\n")

        test_users_cannot_delete_other_users_tasks()
        print("PASS: Test T036 - Users cannot delete other users' tasks\n")

        print("ALL SECURITY TESTS PASSED! User data isolation is working correctly.")

    finally:
        # Clean up test data
        cleanup_test_data()
        print("🧹 Test data cleaned up.")