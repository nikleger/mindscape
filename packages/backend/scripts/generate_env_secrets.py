#!/usr/bin/env python3
"""
Script to generate secure values for environment variables.
Run this script when setting up a new environment to generate secure secrets.
"""

import secrets
import argparse
from pathlib import Path

def generate_secret(length: int = 32) -> str:
    """Generate a secure secret using secrets module."""
    return secrets.token_urlsafe(length)

def main():
    parser = argparse.ArgumentParser(description='Generate secure environment secrets')
    parser.add_argument('--env-file', type=str, default='.env',
                       help='Path to .env file (default: .env)')
    args = parser.parse_args()

    # Generate secrets
    secrets_dict = {
        'SECRET_KEY': generate_secret(32),
        'JWT_SECRET_KEY': generate_secret(32),
        'POSTGRES_PASSWORD': generate_secret(16),
        'REDIS_PASSWORD': generate_secret(16),
    }

    env_path = Path(args.env_file)
    if env_path.exists():
        print(f"Warning: {args.env_file} already exists. Generated values will be printed only.")
        print("\nGenerated secure values (please update your .env file manually):")
        for key, value in secrets_dict.items():
            print(f"{key}={value}")
    else:
        # Start with example template
        example_path = Path('.env.example')
        if example_path.exists():
            content = example_path.read_text()
        else:
            content = ""

        # Replace default values with generated secrets
        for key, value in secrets_dict.items():
            if key in content:
                content = content.replace(f"{key}=your-{key.lower()}-here", f"{key}={value}")
                content = content.replace(f"{key}=your_{key.lower()}_here", f"{key}={value}")

        # Write the new .env file
        env_path.write_text(content)
        print(f"Created {args.env_file} with secure values")
        print("\nGenerated secrets (saved to .env):")
        for key, value in secrets_dict.items():
            print(f"{key}={value}")

if __name__ == '__main__':
    main() 