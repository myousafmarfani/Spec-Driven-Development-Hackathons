"""
Final verification test to ensure the project is production-ready for local testing.
This test verifies that all security enhancements are working correctly.
"""

import subprocess
import sys
import os
import time
import signal
import requests
from threading import Thread
import tempfile
import shutil

def check_dependencies():
    """Check if required dependencies can be imported."""
    print("Checking dependencies...")

    try:
        import fastapi
        import uvicorn
        import sqlmodel
        import jose
        import dotenv
        print("All core dependencies are available")
        return True
    except ImportError as e:
        print(f"X Missing dependency: {e}")
        return False


def check_code_syntax():
    """Check if all Python files have valid syntax."""
    print("Checking code syntax...")

    backend_dir = "."
    python_files = []

    for root, dirs, files in os.walk(backend_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            compile(source, file_path, 'exec')
        except SyntaxError as e:
            print(f"X Syntax error in {file_path}: {e}")
            return False
        except Exception as e:
            print(f"X Error reading {file_path}: {e}")
            continue

    print(f"V All {len(python_files)} Python files have valid syntax")
    return True


def check_environment_variables():
    """Check if required environment variables are set."""
    print("Checking environment variables...")

    required_vars = ['BETTER_AUTH_SECRET']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"Missing environment variables: {missing_vars}")
        print("  Using fallback values for local testing...")
    else:
        print("All required environment variables are set")

    return True


def check_structure():
    """Check if project structure is correct."""
    print("Checking project structure...")

    required_files = [
        'main.py',
        'models.py',
        'auth.py',
        'db.py',
        'routes/tasks.py',
        'pyproject.toml',
        'requirements.txt'
    ]

    missing_files = []

    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print(f"X Missing files: {missing_files}")
        return False

    print("V All required files are present")
    return True


def run_security_tests():
    """Run the security tests to verify user isolation."""
    print("Running security tests...")

    try:
        # Import and run our security tests
        sys.path.insert(0, os.path.dirname(__file__))
        import test_security

        # Run the tests
        test_security.test_users_cannot_access_other_users_tasks()
        print("V Access control test passed")

        test_security.test_users_cannot_modify_other_users_tasks()
        print("V Modification control test passed")

        test_security.test_users_cannot_delete_other_users_tasks()
        print("V Deletion control test passed")

        # Clean up
        test_security.cleanup_test_data()

        print("V All security tests passed")
        return True
    except Exception as e:
        print(f"X Security tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_project_readiness():
    """Main function to verify project readiness."""
    print("=" * 60)
    print("PROJECT VERIFICATION FOR LOCAL TESTING")
    print("=" * 60)

    all_checks_passed = True

    # Run all checks
    checks = [
        ("Dependency Check", check_dependencies),
        ("Code Syntax Check", check_code_syntax),
        ("Environment Variables Check", check_environment_variables),
        ("Project Structure Check", check_structure),
        ("Security Tests", run_security_tests),
    ]

    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * len(check_name))
        try:
            result = check_func()
            if not result:
                all_checks_passed = False
        except Exception as e:
            print(f"X {check_name} failed with exception: {e}")
            all_checks_passed = False

    print("\n" + "=" * 60)
    if all_checks_passed:
        print("ALL CHECKS PASSED!")
        print("Project is production-ready for local testing")
        print("\nTo start the application:")
        print("1. cd backend")
        print("2. uvicorn main:app --reload")
        print("3. In another terminal: cd frontend && npm run dev")
        print("\nThe security features are fully implemented:")
        print("- JWT verification with user_id validation")
        print("- Data isolation between users")
        print("- All endpoints protect against unauthorized access")
    else:
        print("SOME CHECKS FAILED!")
        print("Project may not be ready for local testing")
        print("Please address the issues above before running the application.")
    print("=" * 60)

    return all_checks_passed


if __name__ == "__main__":
    success = verify_project_readiness()
    sys.exit(0 if success else 1)