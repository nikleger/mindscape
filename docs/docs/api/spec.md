# API Specification

## Overview

This document provides the API specification for the Mindscape platform.

## Related Documents

### Strategy Documents
- [Meta Strategy](../../strategy/META_STRATEGY) - Project overview
- [Architecture Decisions](../../strategy/ARCHITECTURE_DECISIONS) - System design
- [Development Strategy](../../strategy/DEVELOPMENT_STRATEGY) - Development process
- [Data Strategy](../../strategy/DATA_STRATEGY) - Data management
- [Security Strategy](../../strategy/SECURITY_STRATEGY) - Security measures

### Technical Documentation
- [Development Guide](../development/DEVELOPMENT_GUIDE) - Setup and workflow
- [Database Schema](../database/DATABASE_SCHEMA) - Database structure
- [Infrastructure Overview](../infrastructure/INFRASTRUCTURE_OVERVIEW) - System architecture

## Base URL

```
https://api.mindscape.io/v1
```

## Authentication

All API requests require authentication using a Bearer token:

```http
Authorization: Bearer <your_token>
```

## Endpoints

### Mind Maps

#### List Mind Maps

```http
GET /mindmaps
```

Response:
```json
{
  "mindmaps": [
    {
      "id": "map_123",
      "title": "Project Planning",
      "created_at": "2024-04-07T10:00:00Z",
      "updated_at": "2024-04-07T11:30:00Z"
    }
  ]
}
```

#### Create Mind Map

```http
POST /mindmaps
```

Request body:
```json
{
  "title": "New Mind Map",
  "description": "Project brainstorming session"
}
```

### Nodes

#### List Nodes

```http
GET /mindmaps/{map_id}/nodes
```

#### Create Node

```http
POST /mindmaps/{map_id}/nodes
```

Request body:
```json
{
  "title": "Main Idea",
  "content": "Central concept",
  "parent_id": "node_123"
}
```

## Error Handling

The API uses standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

API requests are limited to 100 requests per minute per API key.

## Versioning

The API is versioned through the URL path. The current version is v1. 
