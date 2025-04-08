# Development Guide

## Overview

This document provides a guide for developers working on the Mindscape platform.

## Related Documents

### Strategy Documents
- [Meta Strategy](../../strategy/META_STRATEGY) - Project overview
- [Architecture Decisions](../../strategy/ARCHITECTURE_DECISIONS) - System design
- [Development Strategy](../../strategy/DEVELOPMENT_STRATEGY) - Development process
- [Data Strategy](../../strategy/DATA_STRATEGY) - Data management
- [Security Strategy](../../strategy/SECURITY_STRATEGY) - Security measures

### Technical Documentation
- [API Specification](../api/API_SPECIFICATION) - API documentation
- [Database Schema](../database/DATABASE_SCHEMA) - Database structure
- [Infrastructure Overview](../infrastructure/INFRASTRUCTURE_OVERVIEW) - System architecture

## Prerequisites

- Node.js (v16 or higher)
- npm (v7 or higher)
- Git

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/mindscape/mindscape.git
   cd mindscape
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Project Structure

- `/src` - Source code
- `/docs` - Documentation
- `/tests` - Test files
- `/public` - Static assets

## Development Workflow

1. Create a new branch for your feature/fix
2. Make your changes
3. Write/update tests
4. Submit a pull request

## Testing

Run tests with:
```bash
npm test
```

## Building

Build the project with:
```bash
npm run build
```

## Contributing

Please read our [Contribution Strategy](../../strategy/CONTRIBUTION_STRATEGY) for details on our code of conduct and the process for submitting pull requests. 
