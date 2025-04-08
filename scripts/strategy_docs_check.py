#!/usr/bin/env python3
import sys
from pathlib import Path
import re
import yaml
import json

REQUIRED_SECTIONS = {
    'SECURITY_STRATEGY.md': [
        'Security Principles',
        'Authentication & Authorization',
        'Data Protection',
        'Network Security',
        'Security Monitoring',
        'Incident Response',
        'Compliance',
        'Security Training'
    ],
    'PERFORMANCE_STRATEGY.md': [
        'Performance Goals',
        'Frontend Performance',
        'Backend Performance',
        'Load Testing',
        'Monitoring',
        'Optimization Techniques',
        'Performance Testing',
        'CI/CD Integration'
    ],
    'DEVELOPMENT_WORKFLOW.md': [
        'Git Workflow',
        'Code Review Process',
        'Development Environment',
        'Quality Gates',
        'Documentation Requirements',
        'Development Process',
        'Release Process',
        'Monitoring & Feedback'
    ],
    'ARCHITECTURE_DECISIONS.md': [
        'Technology Stack',
        'Project Structure',
        'Authentication Strategy',
        'Database Design',
        'API Design',
        'State Management',
        'Testing Strategy',
        'Performance Strategy'
    ]
}

def check_file_structure(file_path: Path) -> list:
    """Check if the file has all required sections."""
    issues = []
    content = file_path.read_text()
    
    # Get required sections for this file
    required_sections = REQUIRED_SECTIONS.get(file_path.name, [])
    
    # Check each required section
    for section in required_sections:
        if not re.search(rf'#{1,2}\s+{section}', content):
            issues.append(f"Missing required section '{section}' in {file_path.name}")
    
    return issues

def check_code_blocks(file_path: Path) -> list:
    """Check if code blocks are properly formatted and valid."""
    issues = []
    content = file_path.read_text()
    
    # Find all code blocks
    code_blocks = re.finditer(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
    
    for block in code_blocks:
        language = block.group(1)
        code = block.group(2)
        
        if not language:
            issues.append(f"Code block missing language specification in {file_path.name}")
            continue
            
        # Validate based on language
        if language.lower() in ['yaml', 'yml']:
            try:
                yaml.safe_load(code)
            except yaml.YAMLError:
                issues.append(f"Invalid YAML in code block in {file_path.name}")
        elif language.lower() in ['json']:
            try:
                json.loads(code)
            except json.JSONDecodeError:
                issues.append(f"Invalid JSON in code block in {file_path.name}")
        elif language.lower() in ['python', 'py']:
            try:
                compile(code, '<string>', 'exec')
            except SyntaxError:
                issues.append(f"Invalid Python syntax in code block in {file_path.name}")
    
    return issues

def check_links(file_path: Path) -> list:
    """Check if all links are valid."""
    issues = []
    content = file_path.read_text()
    
    # Find all markdown links
    links = re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', content)
    
    for link in links:
        target = link.group(2)
        if target.startswith(('http://', 'https://')):
            continue  # Skip external links
        
        # Check internal links
        if target.startswith('#'):
            # Check if header exists
            header = target[1:].lower().replace('-', ' ')
            if not re.search(rf'#{1,6}\s+{re.escape(header)}', content, re.IGNORECASE):
                issues.append(f"Broken internal link to '{header}' in {file_path.name}")
        else:
            # Check if file exists
            target_path = Path(target)
            if not target_path.exists():
                issues.append(f"Broken file link to '{target}' in {file_path.name}")
    
    return issues

def check_mermaid_diagrams(file_path: Path) -> list:
    """Check if Mermaid diagrams are valid."""
    issues = []
    content = file_path.read_text()
    
    # Find all Mermaid diagrams
    diagrams = re.finditer(r'```mermaid\n(.*?)```', content, re.DOTALL)
    
    for diagram in diagrams:
        diagram_content = diagram.group(1)
        
        # Basic validation of diagram syntax
        if not any(diagram_content.strip().startswith(keyword) for keyword in 
                  ['graph', 'sequenceDiagram', 'classDiagram', 'stateDiagram', 'gantt', 'pie']):
            issues.append(f"Invalid Mermaid diagram syntax in {file_path.name}")
            
        # Check for common syntax errors
        if '-->' in diagram_content and not re.search(r'\w+\s*-->\s*\w+', diagram_content):
            issues.append(f"Malformed relationship in Mermaid diagram in {file_path.name}")
    
    return issues

def check_consistency(files: list[Path]) -> list:
    """Check for consistency across strategy documents."""
    issues = []
    
    # Check for consistent terminology
    terms = {}
    for file in files:
        content = file.read_text()
        
        # Extract defined terms (assuming they're in bold or headings)
        found_terms = re.finditer(r'(?:\*\*|#{1,6}\s+)([A-Z][A-Za-z\s]+)(?:\*\*|$)', content)
        
        for term in found_terms:
            term_text = term.group(1)
            if term_text in terms and terms[term_text] != file:
                # Check if the term is used consistently
                other_content = terms[term_text].read_text()
                if not re.search(rf'\b{re.escape(term_text)}\b', other_content):
                    issues.append(f"Inconsistent use of term '{term_text}' across {file.name} and {terms[term_text].name}")
            terms[term_text] = file
    
    return issues

def main():
    all_issues = []
    strategy_dir = Path('docs/strategy')
    
    if not strategy_dir.exists():
        print("Strategy docs directory not found!")
        sys.exit(1)
    
    strategy_files = list(strategy_dir.glob('*.md'))
    
    for file in strategy_files:
        # Run all checks
        all_issues.extend(check_file_structure(file))
        all_issues.extend(check_code_blocks(file))
        all_issues.extend(check_links(file))
        all_issues.extend(check_mermaid_diagrams(file))
    
    # Run consistency check across all files
    all_issues.extend(check_consistency(strategy_files))
    
    if all_issues:
        print("\nStrategy documentation issues found:")
        for issue in all_issues:
            print(f"- {issue}")
        sys.exit(1)
    
    print("Strategy documentation check passed!")
    sys.exit(0)

if __name__ == '__main__':
    main() 