# Database Schema

## Overview

This document provides the database schema for the Mindscape platform.

## Related Documents

### Strategy Documents
- [Meta Strategy](../../strategy/META_STRATEGY) - Project overview
- [Architecture Decisions](../../strategy/ARCHITECTURE_DECISIONS) - System design
- [Development Strategy](../../strategy/DEVELOPMENT_STRATEGY) - Development process
- [Data Strategy](../../strategy/DATA_STRATEGY) - Data management
- [Security Strategy](../../strategy/SECURITY_STRATEGY) - Security measures

### Technical Documentation
- [Development Guide](../development/DEVELOPMENT_GUIDE) - Setup and workflow
- [API Specification](../api/API_SPECIFICATION) - API documentation
- [Infrastructure Overview](../infrastructure/INFRASTRUCTURE_OVERVIEW) - System architecture

Mindscape uses PostgreSQL as its primary database. The schema is designed to support mind mapping features while maintaining data integrity and performance.

## Tables

### Users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Mind Maps

```sql
CREATE TABLE mind_maps (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Nodes

```sql
CREATE TABLE nodes (
    id UUID PRIMARY KEY,
    mind_map_id UUID REFERENCES mind_maps(id),
    parent_id UUID REFERENCES nodes(id),
    title VARCHAR(255) NOT NULL,
    content TEXT,
    position JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Collaborators

```sql
CREATE TABLE collaborators (
    mind_map_id UUID REFERENCES mind_maps(id),
    user_id UUID REFERENCES users(id),
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (mind_map_id, user_id)
);
```

## Indexes

```sql
CREATE INDEX idx_nodes_mind_map_id ON nodes(mind_map_id);
CREATE INDEX idx_nodes_parent_id ON nodes(parent_id);
CREATE INDEX idx_mind_maps_owner_id ON mind_maps(owner_id);
```

## Triggers

```sql
CREATE TRIGGER update_timestamp
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## Migrations

Database migrations are managed using [Prisma](https://www.prisma.io/). Migration files are stored in the `/prisma/migrations` directory.

## Backup and Recovery

Regular backups are performed daily and stored in a secure location. The backup retention period is 30 days. 
