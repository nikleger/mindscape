#!/bin/bash

# Setup GitHub Repository Script

# Configuration
REPO_NAME="mindscape"
ORGANIZATION="your-org"
BRANCH_PROTECTION=true
DEFAULT_BRANCH="main"

# Create GitHub repository
echo "Creating GitHub repository..."
gh repo create $ORGANIZATION/$REPO_NAME --public --description "Enterprise mind mapping platform" --confirm

# Initialize local repository
echo "Initializing local repository..."
git init
git add .
git commit -m "Initial commit: Project setup"

# Set up remote and push
echo "Setting up remote and pushing initial commit..."
git remote add origin https://github.com/$ORGANIZATION/$REPO_NAME.git
git branch -M $DEFAULT_BRANCH
git push -u origin $DEFAULT_BRANCH

# Create develop branch
echo "Creating develop branch..."
git checkout -b develop
git push -u origin develop

if [ "$BRANCH_PROTECTION" = true ]; then
    echo "Setting up branch protection rules..."
    
    # Protect main branch
    gh api -X PUT "repos/$ORGANIZATION/$REPO_NAME/branches/$DEFAULT_BRANCH/protection" \
        -H "Accept: application/vnd.github.v3+json" \
        --input - << EOF
    {
        "required_status_checks": {
            "strict": true,
            "contexts": ["ci"]
        },
        "enforce_admins": true,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews": true,
            "require_code_owner_reviews": false
        },
        "restrictions": null,
        "allow_force_pushes": false,
        "allow_deletions": false
    }
EOF

    # Protect develop branch
    gh api -X PUT "repos/$ORGANIZATION/$REPO_NAME/branches/develop/protection" \
        -H "Accept: application/vnd.github.v3+json" \
        --input - << EOF
    {
        "required_status_checks": {
            "strict": true,
            "contexts": ["ci"]
        },
        "enforce_admins": true,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews": true,
            "require_code_owner_reviews": false
        },
        "restrictions": null,
        "allow_force_pushes": false,
        "allow_deletions": false
    }
EOF
fi

# Create PR template
echo "Creating PR template..."
mkdir -p .github/pull_request_template
cat > .github/pull_request_template/pull_request_template.md << EOF
# Pull Request

## Description
Please include a summary of the change and which issue is fixed. Please also include relevant motivation and context.

## Type of change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules

## Related Issues
Closes #<issue_number>
EOF

# Create issue templates
echo "Creating issue templates..."
mkdir -p .github/ISSUE_TEMPLATE

# Bug report template
cat > .github/ISSUE_TEMPLATE/bug_report.md << EOF
---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows, macOS]
 - Browser: [e.g. chrome, safari]
 - Version: [e.g. 22]

**Additional context**
Add any other context about the problem here.
EOF

# Feature request template
cat > .github/ISSUE_TEMPLATE/feature_request.md << EOF
---
name: Feature request
about: Suggest an idea for this project
title: ''
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
EOF

# Push templates
echo "Pushing templates..."
git add .github/
git commit -m "Add PR and issue templates"
git push

echo "Repository setup complete!" 