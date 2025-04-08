#!/usr/bin/env python3
import sys
from pathlib import Path
import yaml
import re
import json

def check_secrets_in_code():
    """Check for potential secrets in code."""
    patterns = [
        r'(?i)(\b(api[_-]?key|secret|password|token)[_-]?[a-z0-9_-]*\s*[=:]\s*[\'"]\w+[\'"])',
        r'(?i)(aws[_-]?access[_-]?key[_-]?id|aws[_-]?secret[_-]?access[_-]?key)',
        r'(?i)(bearer\s+[a-z0-9\-\._]+)',
    ]
    
    issues = []
    for file in Path('.').rglob('*'):
        if file.is_file() and file.suffix in ['.py', '.js', '.ts', '.json', '.yaml', '.yml']:
            content = file.read_text()
            for pattern in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    issues.append(f"Potential secret found in {file}: {match.group()}")
    return issues

def check_security_headers():
    """Check for security headers in FastAPI app."""
    issues = []
    main_file = Path('app/main.py')
    if main_file.exists():
        content = main_file.read_text()
        required_headers = [
            'X-Frame-Options',
            'X-Content-Type-Options',
            'X-XSS-Protection',
            'Strict-Transport-Security',
            'Content-Security-Policy',
        ]
        for header in required_headers:
            if header not in content:
                issues.append(f"Missing security header: {header}")
    return issues

def check_auth_config():
    """Check authentication configuration."""
    issues = []
    auth_file = Path('app/core/auth.py')
    if auth_file.exists():
        content = auth_file.read_text()
        required_configs = [
            'JWT_ALGORITHM',
            'ACCESS_TOKEN_EXPIRE_MINUTES',
            'REFRESH_TOKEN_EXPIRE_DAYS',
        ]
        for config in required_configs:
            if config not in content:
                issues.append(f"Missing auth config: {config}")
    return issues

def check_security_dependencies():
    """Check security-related dependencies."""
    issues = []
    requirements_file = Path('requirements.txt')
    if requirements_file.exists():
        content = requirements_file.read_text()
        required_deps = [
            'python-jose[cryptography]',
            'passlib[bcrypt]',
            'python-multipart',
        ]
        for dep in required_deps:
            if dep not in content:
                issues.append(f"Missing security dependency: {dep}")
    return issues

def main():
    all_issues = []
    
    # Run all checks
    all_issues.extend(check_secrets_in_code())
    all_issues.extend(check_security_headers())
    all_issues.extend(check_auth_config())
    all_issues.extend(check_security_dependencies())
    
    if all_issues:
        print("\nSecurity issues found:")
        for issue in all_issues:
            print(f"- {issue}")
        sys.exit(1)
    
    print("Security check passed!")
    sys.exit(0)

if __name__ == '__main__':
    main() 