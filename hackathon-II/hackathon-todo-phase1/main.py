#!/usr/bin/env python3
"""
Main entry point for the Todo Application.

This module initializes and runs the CLI interface for the todo application.
"""

from src.cli.interface import CLIInterface


def main():
    """Main entry point for the application."""
    print("Initializing Todo Application...")
    cli = CLIInterface()
    cli.run()


if __name__ == "__main__":
    main()