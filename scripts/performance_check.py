#!/usr/bin/env python3
import sys
from pathlib import Path
import ast
import re

def check_database_queries():
    """Check for potential database performance issues."""
    issues = []
    for file in Path('.').rglob('*.py'):
        if file.is_file():
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    
                    # Check for N+1 query patterns
                    for node in ast.walk(tree):
                        if isinstance(node, ast.For):
                            if isinstance(node.body[0], ast.Expr):
                                if isinstance(node.body[0].value, ast.Call):
                                    if hasattr(node.body[0].value.func, 'attr'):
                                        if node.body[0].value.func.attr in ['query', 'filter']:
                                            issues.append(f"Potential N+1 query in {file}")
                    
                    # Check for missing indexes
                    if 'filter(' in content and 'Index(' not in content:
                        issues.append(f"Potential missing index in {file}")
            except:
                pass
    return issues

def check_frontend_performance():
    """Check for frontend performance issues."""
    issues = []
    
    # Check Next.js config
    next_config = Path('next.config.js')
    if next_config.exists():
        content = next_config.read_text()
        optimizations = [
            'optimizeCss',
            'optimizeImages',
            'optimizeFonts',
        ]
        for opt in optimizations:
            if opt not in content:
                issues.append(f"Missing Next.js optimization: {opt}")
    
    # Check React components
    for file in Path('.').rglob('*.tsx'):
        if file.is_file():
            content = file.read_text()
            # Check for missing memo
            if 'export default function' in content and 'memo(' not in content:
                issues.append(f"Consider using React.memo for component in {file}")
            # Check for missing keys in lists
            if '.map(' in content and 'key=' not in content:
                issues.append(f"Missing key prop in mapped elements in {file}")
    
    return issues

def check_caching_strategy():
    """Check for caching implementation."""
    issues = []
    
    # Check Redis configuration
    redis_config = Path('app/core/cache.py')
    if redis_config.exists():
        content = redis_config.read_text()
        required_configs = [
            'CACHE_TTL',
            'CACHE_PREFIX',
            'CACHE_URL',
        ]
        for config in required_configs:
            if config not in content:
                issues.append(f"Missing cache config: {config}")
    
    # Check API endpoints for caching
    for file in Path('app/api').rglob('*.py'):
        if file.is_file():
            content = file.read_text()
            if '@router.get' in content and '@cache' not in content:
                issues.append(f"Consider adding cache decorator to GET endpoints in {file}")
    
    return issues

def check_api_performance():
    """Check API performance configurations."""
    issues = []
    
    # Check FastAPI config
    main_file = Path('app/main.py')
    if main_file.exists():
        content = main_file.read_text()
        if 'ORJSONResponse' not in content:
            issues.append("Consider using ORJSONResponse for better JSON performance")
        if 'middleware' in content and 'GZipMiddleware' not in content:
            issues.append("Consider adding GZip compression middleware")
    
    # Check endpoint response size
    for file in Path('app/api').rglob('*.py'):
        if file.is_file():
            content = file.read_text()
            if 'return' in content and 'limit' not in content.lower():
                issues.append(f"Consider adding pagination/limit to responses in {file}")
    
    return issues

def check_resource_optimization():
    """Check for resource optimization issues."""
    issues = []
    
    # Check image optimization
    for file in Path('.').rglob('*.{png,jpg,jpeg}'):
        if file.stat().st_size > 1_000_000:  # 1MB
            issues.append(f"Large image file found: {file}")
    
    # Check bundle optimization
    package_json = Path('package.json')
    if package_json.exists():
        content = package_json.read_text()
        if '"sideEffects": false' not in content:
            issues.append("Consider adding sideEffects: false for better tree-shaking")
    
    return issues

def main():
    all_issues = []
    
    # Run all checks
    all_issues.extend(check_database_queries())
    all_issues.extend(check_frontend_performance())
    all_issues.extend(check_caching_strategy())
    all_issues.extend(check_api_performance())
    all_issues.extend(check_resource_optimization())
    
    if all_issues:
        print("\nPerformance issues found:")
        for issue in all_issues:
            print(f"- {issue}")
        sys.exit(1)
    
    print("Performance check passed!")
    sys.exit(0)

if __name__ == '__main__':
    main() 