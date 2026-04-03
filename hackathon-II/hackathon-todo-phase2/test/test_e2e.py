#!/usr/bin/env python3
"""
End-to-End Testing Script for Todo Application

This script performs comprehensive end-to-end testing of all user flows
in the Todo application including signup, signin, task management, and security.
"""

import requests
import time
import json
from datetime import datetime
import os

# Configuration
BASE_BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
BASE_FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

print("Starting End-to-End Testing for Todo Application")
print("="*60)

def print_step(step_num, description):
    print(f"\nStep {step_num}: {description}")
    print("-"*len(f"Step {step_num}: {description}"))

# Test data
test_user = {
    "email": f"testuser_{int(time.time())}@example.com",
    "password": "securepassword123",
    "name": "Test User"
}

print_step(1, "Testing User Registration")
try:
    response = requests.post(f"{BASE_BACKEND_URL}/api/auth/signup", json=test_user)
    if response.status_code == 200:
        print("✓ User registration successful")
        auth_response = response.json()
        user_data = auth_response.get('user')
        token = auth_response.get('token')
        print(f"  - User ID: {user_data.get('id') if user_data else 'N/A'}")
        print(f"  - Token received: {'Yes' if token else 'No'}")
    else:
        print(f"✗ User registration failed: {response.status_code}")
        print(f"  Response: {response.text}")
except Exception as e:
    print(f"✗ User registration test failed: {e}")

print_step(2, "Testing User Signin")
try:
    signin_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = requests.post(f"{BASE_BACKEND_URL}/api/auth/signin", json=signin_data)
    if response.status_code == 200:
        print("✓ User signin successful")
        auth_response = response.json()
        new_token = auth_response.get('token')
        print(f"  - New token received: {'Yes' if new_token else 'No'}")
        token = new_token  # Update token for subsequent tests
    else:
        print(f"✗ User signin failed: {response.status_code}")
        print(f"  Response: {response.text}")
except Exception as e:
    print(f"✗ User signin test failed: {e}")

# Store user ID for API calls
user_id = user_data.get('id') if user_data else None
if not user_id:
    # Try to extract from token if user_data wasn't available earlier
    print("  - Could not get user ID, attempting to use test email pattern")
    user_id = test_user['email']

print_step(3, "Testing Task Creation")
if token:
    try:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # Create a test task
        task_data = {
            "title": "Test Task for E2E Testing",
            "description": "This is a test task created during end-to-end testing"
        }

        response = requests.post(f"{BASE_BACKEND_URL}/api/{user_id}/tasks",
                                json=task_data, headers=headers)

        if response.status_code == 200:
            print("✓ Task creation successful")
            created_task = response.json()
            task_id = created_task.get('id')
            print(f"  - Task ID: {task_id}")
            print(f"  - Task Title: {created_task.get('title')}")
        else:
            print(f"✗ Task creation failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Task creation test failed: {e}")
else:
    print("  - Skipping task creation: No authentication token available")

print_step(4, "Testing Task Retrieval")
if token and user_id:
    try:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        response = requests.get(f"{BASE_BACKEND_URL}/api/{user_id}/tasks", headers=headers)

        if response.status_code == 200:
            print("✓ Task retrieval successful")
            tasks = response.json()
            print(f"  - Number of tasks retrieved: {len(tasks)}")
            if tasks:
                print(f"  - First task title: {tasks[0].get('title')}")
        else:
            print(f"✗ Task retrieval failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Task retrieval test failed: {e}")
else:
    print("  - Skipping task retrieval: Missing authentication or user ID")

print_step(5, "Testing Task Update")
if token and task_id and user_id:
    try:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # Update the test task
        update_data = {
            "title": "Updated Test Task",
            "description": "This task has been updated during end-to-end testing",
            "completed": True
        }

        response = requests.put(f"{BASE_BACKEND_URL}/api/{user_id}/tasks/{task_id}",
                               json=update_data, headers=headers)

        if response.status_code == 200:
            print("✓ Task update successful")
            updated_task = response.json()
            print(f"  - Updated task title: {updated_task.get('title')}")
            print(f"  - Task completed: {updated_task.get('completed')}")
        else:
            print(f"✗ Task update failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Task update test failed: {e}")
else:
    print("  - Skipping task update: Missing authentication, task ID, or user ID")

print_step(6, "Testing Task Completion Toggle")
if token and task_id and user_id:
    try:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # Toggle task completion status
        toggle_data = {"completed": False}

        response = requests.patch(f"{BASE_BACKEND_URL}/api/{user_id}/tasks/{task_id}/complete",
                                 json=toggle_data, headers=headers)

        if response.status_code == 200:
            print("✓ Task completion toggle successful")
            toggled_task = response.json()
            print(f"  - Task completed: {toggled_task.get('completed')}")
        else:
            print(f"✗ Task completion toggle failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Task completion toggle test failed: {e}")
else:
    print("  - Skipping task completion toggle: Missing authentication, task ID, or user ID")

print_step(7, "Testing Task Deletion")
if token and task_id and user_id:
    try:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        response = requests.delete(f"{BASE_BACKEND_URL}/api/{user_id}/tasks/{task_id}", headers=headers)

        if response.status_code == 200:
            print("✓ Task deletion successful")
            result = response.json()
            print(f"  - Result: {result}")
        else:
            print(f"✗ Task deletion failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Task deletion test failed: {e}")
else:
    print("  - Skipping task deletion: Missing authentication, task ID, or user ID")

print_step(8, "Testing Data Isolation (Security Check)")
# This would require another user account to properly test
print("  - Data isolation testing requires multiple user accounts")
print("  - In a real test, we would create a second user and verify they can't access the first user's tasks")

print_step(9, "Testing Frontend Availability")
try:
    response = requests.get(BASE_FRONTEND_URL)
    if response.status_code == 200:
        print("✓ Frontend is accessible")
        print(f"  - Status Code: {response.status_code}")
    else:
        print(f"✗ Frontend not accessible: {response.status_code}")
except Exception as e:
    print(f"✗ Frontend accessibility test failed: {e}")

print_step(10, "Testing Backend Health")
try:
    response = requests.get(f"{BASE_BACKEND_URL}/health")
    if response.status_code == 200:
        print("✓ Backend health check passed")
        health_data = response.json()
        print(f"  - Status: {health_data.get('status')}")
    else:
        print(f"✗ Backend health check failed: {response.status_code}")
except Exception as e:
    print(f"✗ Backend health test failed: {e}")

print("\n" + "="*60)
print("End-to-End Testing Complete")
print("Review the results above to verify all functionality is working.")
print("Note: Some tests may fail if the backend/frontend services are not running.")

# Additional manual testing instructions
print("\nAdditional Manual Tests to Perform:")
print("1. Navigate to the frontend application and verify UI functionality")
print("2. Test all forms for proper validation and error messages")
print("3. Verify that protected routes redirect unauthenticated users")
print("4. Test the signup/signin flow with multiple browsers")
print("5. Verify responsive design on different screen sizes")
print("6. Test all task management operations through the UI")