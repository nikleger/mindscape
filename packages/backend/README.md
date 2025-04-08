# Mindscape Backend

## Overview
The Mindscape backend is built with FastAPI and provides the core API services for the Mindscape application. It uses Supabase for database management and includes features for authentication, data management, and real-time updates.

## Development Setup

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 15 or higher
- Redis (optional, for caching)
- PowerShell (for Windows development)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/mindscape.git
   cd mindscape/packages/backend
   ```

2. **Set up environment**
   ```powershell
   # Copy environment template
   Copy-Item .env.example .env
   
   # Edit .env with your configuration
   # Update database credentials and Supabase settings
   ```

3. **Start development server**
   ```powershell
   .\start-dev.ps1
   ```

### Database Setup

1. **Local Development**
   ```sql
   -- Create development database
   CREATE DATABASE mindscape_dev;
   
   -- Create test database
   CREATE DATABASE mindscape_test;
   ```

2. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

### API Documentation
Once the server is running, visit:
- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc Documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```
backend/
├── app/
│   ├── api/           # API routes
│   ├── core/          # Core functionality
│   ├── models/        # Database models
│   ├── schemas/       # Pydantic schemas
│   └── services/      # Business logic
├── migrations/        # Database migrations
├── scripts/           # Utility scripts
└── tests/            # Test suite
```

## Development Workflow

1. **Create a new feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Run tests**
   ```bash
   pytest
   ```

3. **Format code**
   ```bash
   black .
   isort .
   ```

4. **Create migration**
   ```bash
   alembic revision --autogenerate -m "description"
   ```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_file.py

# Run with coverage
pytest --cov=app
```

### Test Database
- Tests use a separate database (`mindscape_test`)
- Database is reset before each test
- Use fixtures for test data

## Deployment

### Production Setup
1. Update `.env` with production settings
2. Set up Supabase project
3. Configure CI/CD pipeline
4. Deploy to production environment

### Environment Variables
See `.env.example` for required variables:
- Database configuration
- Security settings
- API keys
- Feature flags

## Contributing

1. Follow the [Agile Strategy](../docs/strategy/AGILE_STRATEGY.md)
2. Write tests for new features
3. Update documentation
4. Submit pull request

## Support

- Documentation: [docs.mindscape.io](https://docs.mindscape.io)
- Issues: [GitHub Issues](https://github.com/your-org/mindscape/issues)
- Discussions: [GitHub Discussions](https://github.com/your-org/mindscape/discussions) 