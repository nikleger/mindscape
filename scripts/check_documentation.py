#!/usr/bin/env python3
import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Any
import yaml
import subprocess
from datetime import datetime
import json

class DocumentationChecker:
    def __init__(self, docs_path: str = "docs"):
        self.docs_path = Path(docs_path)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "summary": {
                "total_files": 0,
                "passed_checks": 0,
                "failed_checks": 0,
                "warnings": 0
            }
        }

    def check_markdown_lint(self) -> Dict[str, Any]:
        """Run markdownlint on documentation files."""
        try:
            result = subprocess.run(
                ["markdownlint", str(self.docs_path), "--config", ".markdownlint.json"],
                capture_output=True,
                text=True
            )
            return {
                "status": "passing" if result.returncode == 0 else "failing",
                "output": result.stdout,
                "errors": result.stderr
            }
        except FileNotFoundError:
            return {
                "status": "error",
                "message": "markdownlint not installed"
            }

    def check_broken_links(self) -> Dict[str, Any]:
        """Check for broken links in documentation."""
        try:
            result = subprocess.run(
                ["markdown-link-check", "-c", ".markdown-link-check.json"],
                capture_output=True,
                text=True
            )
            return {
                "status": "passing" if result.returncode == 0 else "failing",
                "output": result.stdout,
                "errors": result.stderr
            }
        except FileNotFoundError:
            return {
                "status": "error",
                "message": "markdown-link-check not installed"
            }

    def check_spelling(self) -> Dict[str, Any]:
        """Run spell checking on documentation files."""
        try:
            result = subprocess.run(
                ["cspell", "**/*.md"],
                capture_output=True,
                text=True
            )
            return {
                "status": "passing" if result.returncode == 0 else "failing",
                "output": result.stdout,
                "errors": result.stderr
            }
        except FileNotFoundError:
            return {
                "status": "error",
                "message": "cspell not installed"
            }

    def check_file_structure(self) -> Dict[str, Any]:
        """Verify documentation file structure and naming conventions."""
        issues = []
        for root, _, files in os.walk(self.docs_path):
            for file in files:
                if file.endswith('.md'):
                    # Check file naming convention
                    if not re.match(r'^[a-z0-9-]+\.md$', file):
                        issues.append(f"Invalid filename: {file}")
                    
                    # Check for required sections
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if not re.search(r'^#\s+.*$', content, re.MULTILINE):
                            issues.append(f"Missing title in {file}")
                        if not re.search(r'##\s+.*$', content, re.MULTILINE):
                            issues.append(f"Missing sections in {file}")

        return {
            "status": "passing" if not issues else "failing",
            "issues": issues
        }

    def check_metadata(self) -> Dict[str, Any]:
        """Verify metadata in documentation files."""
        issues = []
        for root, _, files in os.walk(self.docs_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Check for last updated date
                        if not re.search(r'last_updated:\s*\d{4}-\d{2}-\d{2}', content):
                            issues.append(f"Missing last_updated date in {file}")
                        # Check for author
                        if not re.search(r'author:\s*.*$', content, re.MULTILINE):
                            issues.append(f"Missing author in {file}")

        return {
            "status": "passing" if not issues else "failing",
            "issues": issues
        }

    def run_checks(self) -> None:
        """Run all documentation checks."""
        checks = {
            "markdown_lint": self.check_markdown_lint,
            "broken_links": self.check_broken_links,
            "spelling": self.check_spelling,
            "file_structure": self.check_file_structure,
            "metadata": self.check_metadata
        }

        for check_name, check_func in checks.items():
            result = check_func()
            self.results["checks"][check_name] = result
            if result["status"] == "passing":
                self.results["summary"]["passed_checks"] += 1
            elif result["status"] == "failing":
                self.results["summary"]["failed_checks"] += 1
            else:
                self.results["summary"]["warnings"] += 1

        self.results["summary"]["total_files"] = len(list(self.docs_path.rglob("*.md")))

    def generate_report(self, output_file: str = "documentation_check_report.json") -> None:
        """Generate a report of the documentation checks."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)

    def print_summary(self) -> None:
        """Print a summary of the documentation checks."""
        print("\nDocumentation Check Summary")
        print("=" * 50)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Total Files: {self.results['summary']['total_files']}")
        print(f"Passed Checks: {self.results['summary']['passed_checks']}")
        print(f"Failed Checks: {self.results['summary']['failed_checks']}")
        print(f"Warnings: {self.results['summary']['warnings']}")
        
        print("\nDetailed Results")
        print("=" * 50)
        for check_name, result in self.results["checks"].items():
            print(f"\n{check_name}:")
            print(f"Status: {result['status']}")
            if "issues" in result and result["issues"]:
                print("Issues:")
                for issue in result["issues"]:
                    print(f"  - {issue}")
            if "errors" in result and result["errors"]:
                print("Errors:")
                print(result["errors"])

def main():
    checker = DocumentationChecker()
    checker.run_checks()
    checker.generate_report()
    checker.print_summary()

    # Exit with error code if any checks failed
    if checker.results["summary"]["failed_checks"] > 0:
        sys.exit(1)

if __name__ == "__main__":
    main() 