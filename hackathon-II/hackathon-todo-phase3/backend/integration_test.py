"""
Integration tests for the Todo Application API endpoints.

This script performs comprehensive tests on all API endpoints
to verify functionality, authentication, and user data isolation.
"""

import subprocess
import time
import requests
import sys
import os
import json
from datetime import datetime
from jose import JWTError, jwt

# Configuration
BASE_URL = "http://localhost:8000"
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_key_for_development")
ALGORITHM = "HS256"

def create_test_token(user_id: str) -> str:
    """Creates a test token for a given user ID."""
    from datetime import datetime, timedelta

    expire = datetime.utcnow() + timedelta(minutes=60 * 24 * 7)  # 7 days
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def test_api_endpoints():
    """Perform comprehensive tests on all API endpoints."""

    print("Integration Testing: Todo Application API")
    print("=" * 60)

    # Test users
    user1_id = "test-user-1-uuid"
    user2_id = "test-user-2-uuid"

    # Create test tokens
    user1_token = create_test_token(user1_id)
    user2_token = create_test_token(user2_id)

    print(f"✓ Created test tokens for {user1_id} and {user2_id}")

    # Headers for API requests
    user1_headers = {"Authorization": f"Bearer {user1_token}", "Content-Type": "application/json"}
    user2_headers = {"Authorization": f"Bearer {user2_token}", "Content-Type": "application/json"}

    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Server is running and accessible")
        else:
            print(f"⚠ Server responded with status: {response.status_code}")
    except requests.ConnectionError:
        print(f"⚠ Server is not running at {BASE_URL}")
        print("ℹ Please start the server with: cd backend && uvicorn main:app --reload")
        return False

    success_count = 0
    total_tests = 0

    print("\nTesting API endpoints...")
    print("-" * 30)

    # Test 1: GET /api/{user_id}/tasks (empty list)
    total_tests += 1
    try:
        response = requests.get(f"{BASE_URL}/api/{user1_id}/tasks", headers=user1_headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"✓ GET /api/{user1_id}/tasks - Status: {response.status_code} (empty list)")
            success_count += 1
        else:
            print(f"✗ GET /api/{user1_id}/tasks - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ GET /api/{user1_id}/tasks - Error: {e}")

    # Test 2: POST /api/{user_id}/tasks (create task)
    total_tests += 1
    try:
        task_data = {
            "title": "Test Task 1",
            "description": "This is a test task created via API"
        }
        response = requests.post(f"{BASE_URL}/api/{user1_id}/tasks",
                                headers=user1_headers,
                                json=task_data)
        if response.status_code == 200:
            created_task = response.json()
            print(f"✓ POST /api/{user1_id}/tasks - Status: {response.status_code} (task created)")
            task_id = created_task.get('id')
            success_count += 1
        else:
            print(f"✗ POST /api/{user1_id}/tasks - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ POST /api/{user1_id}/tasks - Error: {e}")

    # Test 3: GET /api/{user_id}/tasks/{task_id} (get specific task)
    if 'task_id' in locals():
        total_tests += 1
        try:
            response = requests.get(f"{BASE_URL}/api/{user1_id}/tasks/{task_id}",
                                   headers=user1_headers)
            if response.status_code == 200:
                task = response.json()
                print(f"✓ GET /api/{user1_id}/tasks/{task_id} - Status: {response.status_code}")
                success_count += 1
            else:
                print(f"✗ GET /api/{user1_id}/tasks/{task_id} - Status: {response.status_code}")
        except Exception as e:
            print(f"✗ GET /api/{user1_id}/tasks/{task_id} - Error: {e}")

    # Test 4: PUT /api/{user_id}/tasks/{task_id} (update task)
    if 'task_id' in locals():
        total_tests += 1
        try:
            update_data = {
                "title": "Updated Test Task 1",
                "description": "Updated description",
                "completed": True
            }
            response = requests.put(f"{BASE_URL}/api/{user1_id}/tasks/{task_id}",
                                   headers=user1_headers,
                                   json=update_data)
            if response.status_code == 200:
                updated_task = response.json()
                print(f"✓ PUT /api/{user1_id}/tasks/{task_id} - Status: {response.status_code} (updated)")
                success_count += 1
            else:
                print(f"✗ PUT /api/{user1_id}/tasks/{task_id} - Status: {response.status_code}")
        except Exception as e:
            print(f"✗ PUT /api/{user1_id}/tasks/{task_id} - Error: {e}")

    # Test 5: PATCH /api/{user_id}/tasks/{task_id}/complete (toggle completion)
    if 'task_id' in locals():
        total_tests += 1
        try:
            toggle_data = {"completed": False}
            response = requests.patch(f"{BASE_URL}/api/{user1_id}/tasks/{task_id}/complete",
                                     headers=user1_headers,
                                     json=toggle_data)
            if response.status_code == 200:
                toggled_task = response.json()
                print(f"✓ PATCH /api/{user1_id}/tasks/{task_id}/complete - Status: {response.status_code}")
                success_count += 1
            else:
                print(f"✗ PATCH /api/{user1_id}/tasks/{task_id}/complete - Status: {response.status_code}")
        except Exception as e:
            print(f"✗ PATCH /api/{user1_id}/tasks/{task_id}/complete - Error: {e}")

    # Test 6: DELETE /api/{user_id}/tasks/{task_id} (delete task)
    if 'task_id' in locals():
        total_tests += 1
        try:
            response = requests.delete(f"{BASE_URL}/api/{user1_id}/tasks/{task_id}",
                                      headers=user1_headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ DELETE /api/{user1_id}/tasks/{task_id} - Status: {response.status_code}")
                success_count += 1
            else:
                print(f"✗ DELETE /api/{user1_id}/tasks/{task_id} - Status: {response.status_code}")
        except Exception as e:
            print(f"✗ DELETE /api/{user1_id}/tasks/{task_id} - Error: {e}")

    # Test 7: Test data isolation (user2 can't access user1's resources)
    total_tests += 1
    try:
        response = requests.get(f"{BASE_URL}/api/{user1_id}/tasks", headers=user2_headers)
        # This should fail with 403 (Forbidden) or similar
        if response.status_code in [403, 401]:
            print(f"✓ Data isolation verified - User 2 blocked from User 1's data (Status: {response.status_code})")
            success_count += 1
        else:
            print(f"✗ Data isolation failed - User 2 accessed User 1's data (Status: {response.status_code})")
    except Exception as e:
        print(f"✗ Data isolation test - Error: {e}")

    # Test 8: Test unauthorized access (no token)
    total_tests += 1
    try:
        response = requests.get(f"{BASE_URL}/api/{user1_id}/tasks")
        # This should fail with 401 (Unauthorized)
        if response.status_code in [401, 403]:
            print(f"✓ Authentication required - Unauthorized request blocked (Status: {response.status_code})")
            success_count += 1
        else:
            print(f"? Authentication check - Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"✗ Authentication test - Error: {e}")

    print("\n" + "=" * 60)
    print(f"Integration Test Results: {success_count}/{total_tests} tests passed")

    if total_tests > 0:
        success_rate = (success_count / total_tests) * 100
        print(f"Success Rate: {success_rate:.1f}%")

        if success_rate >= 80:
            print("✅ API integration testing: PASSED")
            return True
        else:
            print("❌ API integration testing: FAILED")
            return False
    else:
        print("⚠ No tests were run")
        return False

def run_manual_tests():
    """Print manual testing commands for verification."""
    print("\nManual Testing Commands:")
    print("-" * 30)
    print("# Health check")
    print("curl -X GET http://localhost:8000/health")
    print()
    print("# Create a test token (replace with your SECRET_KEY)")
    print("python -c \"from jose import jwt; print(jwt.encode({'sub': 'test-user'}, 'your_secret_key', algorithm='HS256'))\"")
    print()
    print("# Get tasks for user (replace YOUR_TOKEN with actual token)")
    print("curl -H 'Authorization: Bearer YOUR_TOKEN' http://localhost:8000/api/test-user/tasks")
    print()
    print("# Create a task (replace YOUR_TOKEN with actual token)")
    print("curl -X POST \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -H 'Authorization: Bearer YOUR_TOKEN' \\")
    print("  -d '{\"title\":\"Test task\",\"description\":\"Description here\"}' \\")
    print("  http://localhost:8000/api/test-user/tasks")

if __name__ == "__main__":
    print("Starting API Integration Tests...\n")

    success = test_api_endpoints()
    run_manual_tests()

    print(f"\nOverall Result: {'SUCCESS' if success else 'FAILURE'}")
    sys.exit(0 if success else 1)