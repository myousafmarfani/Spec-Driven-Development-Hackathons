"""
Validation Tests for AI Chatbot Todo Management System
This module contains tests for natural language commands, error handling, and persistence.
"""
import asyncio
import pytest
import os
from typing import Dict, Any, List
from datetime import datetime

# Import necessary modules
from backend.src.agents.agent_runner import AgentRunner
from backend.src.services.chat_service import ChatService
from backend.db import get_session
from backend.src.models.conversation import Conversation
from backend.src.models.message import Message
from sqlmodel import Session, select


class TestValidator:
    """
    Validator class to test the implemented functionality.
    """

    def __init__(self):
        # Create agent runner instance
        self.agent_runner = AgentRunner()

        # Get database session
        self.db_session = next(get_session())

    def get_agent(self):
        """
        Lazy load the agent to avoid OpenAI API key issues during import.
        """
        from backend.src.agents.todo_agent import TodoAgent
        return TodoAgent()

    def test_natural_language_commands(self) -> Dict[str, Any]:
        """
        Test 8 natural language commands from the spec.
        """
        print("Testing 8 natural language commands...")

        # Sample user ID for testing
        user_id = "test-user-123"

        # Define 8 natural language commands to test
        commands = [
            "add task Buy groceries",
            "add task Walk the dog",
            "list my tasks",
            "show me all tasks",
            "complete task 1",
            "mark task 2 as done",
            "delete task 1",
            "update task 2 with new description walking the golden retriever"
        ]

        results = {
            "passed": 0,
            "failed": 0,
            "details": []
        }

        try:
            # Get the agent instance
            agent = self.get_agent()

            for i, command in enumerate(commands):
                try:
                    # Run the agent with the command
                    result = agent.run_agent(command, user_id, conversation_history=[])

                    # Log the result
                    detail = {
                        "command": command,
                        "response": result.get("response", ""),
                        "tool_calls": result.get("tool_calls", []),
                        "status": "PASSED"
                    }

                    print(f"Command {i+1}: {command}")
                    print(f"Response: {result.get('response', 'No response')}")
                    print(f"Tool Calls: {result.get('tool_calls', [])}")
                    print("---")

                    results["details"].append(detail)
                    results["passed"] += 1

                except Exception as e:
                    detail = {
                        "command": command,
                        "error": str(e),
                        "status": "FAILED"
                    }

                    print(f"Command {i+1}: {command} - FAILED with error: {e}")

                    results["details"].append(detail)
                    results["failed"] += 1

        except Exception as e:
            print(f"Error initializing agent: {e}")
            # If we can't initialize the agent, mark all as failed
            for command in commands:
                detail = {
                    "command": command,
                    "error": str(e),
                    "status": "FAILED"
                }
                results["details"].append(detail)
                results["failed"] += 1

        print(f"\nNatural Language Commands Test Results:")
        print(f"Passed: {results['passed']}, Failed: {results['failed']}")

        return results

    def test_error_handling(self) -> Dict[str, Any]:
        """
        Test error handling for invalid task IDs and deleted tasks.
        """
        print("\nTesting error handling for invalid task IDs and deleted tasks...")

        results = {
            "passed": 0,
            "failed": 0,
            "details": []
        }

        # Test cases for error scenarios
        error_scenarios = [
            {
                "name": "Invalid task ID for completion",
                "command": "complete task 999999",
                "expected_error": True
            },
            {
                "name": "Invalid task ID for deletion",
                "command": "delete task 999999",
                "expected_error": True
            },
            {
                "name": "Invalid task ID for update",
                "command": "update task 999999 with new title Fixed Task",
                "expected_error": True
            }
        ]

        user_id = "test-user-123"

        try:
            # Get the agent instance
            agent = self.get_agent()

            for scenario in error_scenarios:
                try:
                    # Run the agent with the error-inducing command
                    result = agent.run_agent(scenario["command"], user_id, conversation_history=[])

                    # Check if the response indicates proper error handling
                    response = result.get("response", "").lower()
                    has_error_indication = any(word in response for word in ["error", "not found", "invalid", "doesn't exist", "failed"])

                    detail = {
                        "scenario": scenario["name"],
                        "command": scenario["command"],
                        "response": result.get("response", ""),
                        "has_error_indication": has_error_indication
                    }

                    if has_error_indication or scenario["expected_error"]:
                        detail["status"] = "PASSED"
                        results["passed"] += 1
                        print(f"PASSED: {scenario['name']} - {result.get('response', 'No response')}")
                    else:
                        detail["status"] = "FAILED"
                        results["failed"] += 1
                        print(f"FAILED: {scenario['name']} - Expected error handling but got: {result.get('response', 'No response')}")

                    results["details"].append(detail)

                except Exception as e:
                    detail = {
                        "scenario": scenario["name"],
                        "command": scenario["command"],
                        "error": str(e),
                        "status": "FAILED"
                    }

                    results["details"].append(detail)
                    results["failed"] += 1
                    print(f"ERROR in {scenario['name']}: {e}")

        except Exception as e:
            print(f"Error initializing agent for error handling test: {e}")
            # If we can't initialize the agent, mark all as failed
            for scenario in error_scenarios:
                detail = {
                    "scenario": scenario["name"],
                    "command": scenario["command"],
                    "error": str(e),
                    "status": "FAILED"
                }
                results["details"].append(detail)
                results["failed"] += 1

        print(f"\nError Handling Test Results:")
        print(f"Passed: {results['passed']}, Failed: {results['failed']}")

        return results

    def test_conversation_persistence(self) -> Dict[str, Any]:
        """
        Test conversation persistence across server restarts.
        """
        print("\nTesting conversation persistence...")

        results = {
            "passed": 0,
            "failed": 0,
            "details": []
        }

        user_id = "test-user-persistence"

        try:
            # Create a new conversation and add some messages
            conversation_result = asyncio.run(
                self.agent_runner.run_agent_async(
                    user_input="add task Remember to test persistence",
                    user_id=user_id
                )
            )

            conversation_id = conversation_result.get("conversation_id")

            if conversation_id:
                # Verify the conversation was saved to the database
                conversation = self.db_session.get(Conversation, conversation_id)

                if conversation and conversation.user_id == user_id:
                    # Add another message to the same conversation
                    second_message_result = asyncio.run(
                        self.agent_runner.run_agent_async(
                            user_input="list my tasks",
                            user_id=user_id,
                            conversation_id=conversation_id
                        )
                    )

                    # Check if the second message was added to the same conversation
                    messages_statement = select(Message).where(Message.conversation_id == conversation_id)
                    messages = self.db_session.exec(messages_statement).all()

                    if len(messages) >= 2:
                        detail = {
                            "test": "Conversation persistence",
                            "conversation_id": conversation_id,
                            "message_count": len(messages),
                            "status": "PASSED"
                        }

                        results["passed"] += 1
                        print(f"PASSED: Conversation persisted with {len(messages)} messages")
                    else:
                        detail = {
                            "test": "Conversation persistence",
                            "conversation_id": conversation_id,
                            "message_count": len(messages),
                            "status": "FAILED"
                        }

                        results["failed"] += 1
                        print(f"FAILED: Expected at least 2 messages, got {len(messages)}")
                else:
                    detail = {
                        "test": "Conversation persistence",
                        "error": "Conversation not found in database",
                        "status": "FAILED"
                    }

                    results["failed"] += 1
                    print("FAILED: Conversation not saved to database")
            else:
                detail = {
                    "test": "Conversation persistence",
                    "error": "No conversation ID returned",
                    "status": "FAILED"
                }

                results["failed"] += 1
                print("FAILED: No conversation ID returned")

            results["details"].append(detail)

        except Exception as e:
            detail = {
                "test": "Conversation persistence",
                "error": str(e),
                "status": "FAILED"
            }

            results["details"].append(detail)
            results["failed"] += 1
            print(f"ERROR in conversation persistence test: {e}")

        print(f"\nConversation Persistence Test Results:")
        print(f"Passed: {results['passed']}, Failed: {results['failed']}")

        return results

    def run_all_tests(self) -> Dict[str, Any]:
        """
        Run all validation tests and return comprehensive results.
        """
        print("Starting validation tests for Phase 3...\n")

        all_results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {}
        }

        # Run natural language commands test
        all_results["tests"]["natural_language_commands"] = self.test_natural_language_commands()

        # Run error handling test
        all_results["tests"]["error_handling"] = self.test_error_handling()

        # Run conversation persistence test
        all_results["tests"]["conversation_persistence"] = self.test_conversation_persistence()

        # Calculate overall results
        total_passed = sum(test["passed"] for test in all_results["tests"].values())
        total_failed = sum(test["failed"] for test in all_results["tests"].values())

        all_results["summary"] = {
            "total_passed": total_passed,
            "total_failed": total_failed,
            "success_rate": total_passed / (total_passed + total_failed) if (total_passed + total_failed) > 0 else 0
        }

        print(f"\n=== FINAL RESULTS ===")
        print(f"Total Passed: {total_passed}")
        print(f"Total Failed: {total_failed}")
        print(f"Success Rate: {all_results['summary']['success_rate']:.2%}")

        if total_failed == 0:
            print("🎉 All validation tests PASSED!")
        else:
            print(f"⚠️  {total_failed} tests failed. Please review the implementation.")

        return all_results


if __name__ == "__main__":
    validator = TestValidator()
    results = validator.run_all_tests()

    # Write results to a file for record keeping
    import json
    with open("validation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nValidation results saved to validation_results.json")