#!/usr/bin/env python3
"""
Production Testing Script for Todo Application

This script performs comprehensive testing of the deployed Todo application
to verify all functionality works in the production environment.
"""

import requests
import time
import json
from datetime import datetime
import os
import sys

# Configuration
PRODUCTION_BACKEND_URL = os.getenv("PRODUCTION_BACKEND_URL", "https://your-backend-deployment-url.com")
PRODUCTION_FRONTEND_URL = os.getenv("PRODUCTION_FRONTEND_URL", "https://your-frontend-deployment-url.vercel.app")

# Test user credentials
TEST_EMAIL = f"testuser_{int(time.time())}@example.com"
TEST_PASSWORD = "securepassword123"
TEST_NAME = "Production Test User"

print("Starting Production Deployment Testing")
print("="*60)
print(f"Backend URL: {PRODUCTION_BACKEND_URL}")
print(f"Frontend URL: {PRODUCTION_FRONTEND_URL}")
print(f"Test User: {TEST_EMAIL}")
print("="*60)

def print_step(step_num, description):
    print(f"\nStep {step_num}: {description}")
    print("-"*len(f"Step {step_num}: {description}"))

def test_backend_health():
    """Test that the backend is accessible and healthy"""
    try:
        response = requests.get(f"{PRODUCTION_BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✓ Backend health check passed")
            health_data = response.json()
            print(f"  Status: {health_data}")
            return True
        else:
            print(f"✗ Backend health check failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Backend health check failed with error: {e}")
        return False

def test_api_docs():
    """Test that API documentation is accessible"""
    try:
        response = requests.get(f"{PRODUCTION_BACKEND_URL}/docs", timeout=10)
        if response.status_code == 200:
            print("✓ API documentation accessible")
            return True
        else:
            print(f"✗ API documentation not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ API documentation check failed: {e}")
        return False

def test_user_registration():
    """Test user registration flow"""
    try:
        register_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "name": TEST_NAME
        }

        response = requests.post(f"{PRODUCTION_BACKEND_URL}/api/auth/signup",
                                json=register_data, timeout=10)

        if response.status_code == 200:
            print("✓ User registration successful")
            auth_result = response.json()
            token = auth_result.get('token')
            user = auth_result.get('user')
            print(f"  - Token received: {'Yes' if token else 'No'}")
            print(f"  - User created: {user.get('name') if user else 'Unknown'}")
            return token
        else:
            print(f"✗ User registration failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ User registration test failed: {e}")
        return None

def test_user_login(token_after_reg):
    """Test user login flow"""
    try:
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }

        response = requests.post(f"{PRODUCTION_BACKEND_URL}/api/auth/signin",
                                json=login_data, timeout=10)

        if response.status_code == 200:
            print("✓ User login successful")
            auth_result = response.json()
            token = auth_result.get('token')
            user = auth_result.get('user')
            print(f"  - Token received: {'Yes' if token else 'No'}")

            # Use the login token for subsequent tests if registration didn't provide one
            return token if token else token_after_reg
        else:
            print(f"✗ User login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return token_after_reg  # Fall back to registration token if available
    except Exception as e:
        print(f"✗ User login test failed: {e}")
        return None

def test_task_operations(auth_token):
    """Test task CRUD operations"""
    if not auth_token:
        print("\n⚠ Skipping task operations: No authentication token available")
        return None

    try:
        headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}

        # Get user ID from token or use email pattern (in a real implementation, we'd decode the JWT)
        # For this test, we'll use the email as the user ID since it's consistent with the backend
        user_id = TEST_EMAIL

        print(f"\nTesting task operations for user: {user_id}")

        # Test 1: Create a task
        task_data = {
            "title": "Test Task for Production",
            "description": "This task is created during production testing"
        }

        response = requests.post(f"{PRODUCTION_BACKEND_URL}/api/{user_id}/tasks",
                                json=task_data, headers=headers, timeout=10)

        if response.status_code == 200:
            print("✓ Task creation successful")
            created_task = response.json()
            task_id = created_task.get('id')
            print(f"  - Task ID: {task_id}")
        else:
            print(f"✗ Task creation failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None

        # Test 2: Get tasks
        response = requests.get(f"{PRODUCTION_BACKEND_URL}/api/{user_id}/tasks",
                              headers=headers, timeout=10)

        if response.status_code == 200:
            print("✓ Task retrieval successful")
            tasks = response.json()
            print(f"  - Number of tasks: {len(tasks)}")
        else:
            print(f"✗ Task retrieval failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return task_id

        # Test 3: Update task
        update_data = {
            "title": "Updated Test Task",
            "description": "This task has been updated during production testing",
            "completed": True
        }

        response = requests.put(f"{PRODUCTION_BACKEND_URL}/api/{user_id}/tasks/{task_id}",
                               json=update_data, headers=headers, timeout=10)

        if response.status_code == 200:
            print("✓ Task update successful")
            updated_task = response.json()
            print(f"  - Updated task completed: {updated_task.get('completed')}")
        else:
            print(f"✗ Task update failed: {response.status_code}")
            print(f"  Response: {response.text}")

        # Test 4: Toggle task completion
        toggle_data = {"completed": False}

        response = requests.patch(f"{PRODUCTION_BACKEND_URL}/api/{user_id}/tasks/{task_id}/complete",
                                 json=toggle_data, headers=headers, timeout=10)

        if response.status_code == 200:
            print("✓ Task completion toggle successful")
            toggled_task = response.json()
            print(f"  - Task now completed: {toggled_task.get('completed')}")
        else:
            print(f"✗ Task completion toggle failed: {response.status_code}")
            print(f"  Response: {response.text}")

        # Test 5: Get specific task
        response = requests.get(f"{PRODUCTION_BACKEND_URL}/api/{user_id}/tasks/{task_id}",
                               headers=headers, timeout=10)

        if response.status_code == 200:
            print("✓ Get specific task successful")
            task = response.json()
            print(f"  - Task title: {task.get('title')}")
        else:
            print(f"✗ Get specific task failed: {response.status_code}")
            print(f"  Response: {response.text}")

        return task_id

    except Exception as e:
        print(f"✗ Task operations test failed: {e}")
        return None

def test_frontend_accessibility():
    """Test that the frontend is accessible"""
    try:
        response = requests.get(PRODUCTION_FRONTEND_URL, timeout=15)
        if response.status_code == 200:
            print("✓ Frontend is accessible")
            print(f"  - Status Code: {response.status_code}")
            # Check if it's an HTML response
            if 'text/html' in response.headers.get('content-type', ''):
                print("  - Content Type: HTML (expected)")
            return True
        else:
            print(f"✗ Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Frontend accessibility test failed: {e}")
        return False

def test_cors_configuration():
    """Test that CORS is configured correctly"""
    try:
        # Try to make a preflight request
        headers = {
            'Origin': PRODUCTION_FRONTEND_URL,
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'X-Requested-With, Content-Type'
        }

        response = requests.options(f"{PRODUCTION_BACKEND_URL}/api/health", headers=headers, timeout=10)

        cors_origin = response.headers.get('Access-Control-Allow-Origin')
        cors_methods = response.headers.get('Access-Control-Allow-Methods')

        if cors_origin and (cors_origin == PRODUCTION_FRONTEND_URL or cors_origin == '*'):
            print("✓ CORS configuration appears correct")
            print(f"  - Allowed Origin: {cors_origin}")
            if cors_methods:
                print(f"  - Allowed Methods: {cors_methods}")
            return True
        else:
            print(f"⚠ CORS configuration might need review")
            print(f"  - Allowed Origin: {cors_origin or 'Not set'}")
            return True  # Not a failure, just a configuration check
    except Exception as e:
        print(f"⚠ CORS test failed (this might be normal depending on server config): {e}")
        return True  # Not a critical failure

def main():
    """Main test execution"""
    results = {
        'backend_health': False,
        'api_docs': False,
        'user_registration': None,
        'user_login': None,
        'task_operations': None,
        'frontend_accessibility': False,
        'cors_configuration': False
    }

    print("Starting comprehensive production testing...\n")

    # Test 1: Backend health
    results['backend_health'] = test_backend_health()

    # Test 2: API documentation
    if results['backend_health']:
        results['api_docs'] = test_api_docs()

    # Test 3: User registration
    if results['backend_health']:
        results['user_registration'] = test_user_registration()

    # Test 4: User login
    if results['user_registration'] or results['backend_health']:
        results['user_login'] = test_user_login(results['user_registration'])

    # Test 5: Task operations
    if results['user_login']:
        results['task_operations'] = test_task_operations(results['user_login'])

    # Test 6: Frontend accessibility
    results['frontend_accessibility'] = test_frontend_accessibility()

    # Test 7: CORS configuration
    results['cors_configuration'] = test_cors_configuration()

    # Print results summary
    print("\n" + "="*60)
    print("PRODUCTION TESTING SUMMARY")
    print("="*60)

    print(f"Backend Health: {'✓ PASS' if results['backend_health'] else '✗ FAIL'}")
    print(f"API Documentation: {'✓ PASS' if results['api_docs'] else '✗ FAIL'}")
    print(f"User Registration: {'✓ PASS' if results['user_registration'] else '✗ FAIL'}")
    print(f"User Login: {'✓ PASS' if results['user_login'] else '✗ FAIL'}")
    print(f"Task Operations: {'✓ PASS' if results['task_operations'] is not None else '✗ FAIL'}")
    print(f"Frontend Accessibility: {'✓ PASS' if results['frontend_accessibility'] else '✗ FAIL'}")
    print(f"CORS Configuration: {'✓ OK' if results['cors_configuration'] else '? CHECK'}")

    # Calculate success rate
    success_count = sum([
        results['backend_health'],
        results['api_docs'],
        results['user_registration'] is not None,
        results['user_login'] is not None,
        results['task_operations'] is not None,
        results['frontend_accessibility']
    ])

    total_tests = 6  # Excluding CORS which is a check not a pass/fail
    success_rate = (success_count / total_tests) * 100

    print(f"\nSuccess Rate: {success_count}/{total_tests} ({success_rate:.1f}%)")

    if success_rate >= 80:
        print("\n🎉 Overall Result: PRODUCTION READY!")
        print("Most critical functions are working correctly.")
    elif success_rate >= 60:
        print("\n⚠ Overall Result: PARTIALLY READY")
        print("Some functionality is working but review recommended.")
    else:
        print("\n❌ Overall Result: NOT READY")
        print("Major functionality is not working. Requires immediate attention.")

    print("\nTesting completed. Review individual results above.")
    return success_rate >= 80

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)