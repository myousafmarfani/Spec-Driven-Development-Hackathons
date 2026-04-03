# Data Model: Full-Stack Todo Web Application

**Created**: 2026-02-08
**Feature**: Full-Stack Todo Web Application
**Input**: Feature specification and research findings

## Entity Definitions

### User
Represents a registered user in the system

**Fields**:
- `id`: string (primary key, UUID, required)
- `email`: string (unique, not null, required, valid email format)
- `name`: string (not null, required, 1-100 characters)
- `password_hash`: string (not null, required, managed by Better Auth)
- `created_at`: datetime (not null, default: current timestamp)
- `updated_at`: datetime (not null, auto-updated on change)

**Validation Rules**:
- Email must be valid email format
- Password must be at least 8 characters (enforced by authentication system)
- Name must be between 1 and 100 characters
- Email must be unique across all users

**Relationships**:
- One-to-many with Task (user can have many tasks)

### Task
Represents a todo item owned by a user

**Fields**:
- `id`: integer (primary key, auto-increment, required)
- `user_id`: string (foreign key to User.id, not null, required)
- `title`: string (not null, required, 1-200 characters)
- `description`: string (nullable, optional, max 1000 characters)
- `completed`: boolean (not null, default: false)
- `created_at`: datetime (not null, default: current timestamp)
- `updated_at`: datetime (not null, auto-updated on change)

**Validation Rules**:
- Title must be between 1 and 200 characters
- Description, if provided, must be max 1000 characters
- User_id must reference an existing user
- Completed field indicates task completion status

**Relationships**:
- Many-to-one with User (many tasks belong to one user)

## Database Schema

### Table: users
Managed by Better Auth with additional custom fields if needed

```
id: UUID (PRIMARY KEY)
email: VARCHAR(255) UNIQUE NOT NULL
name: VARCHAR(100) NOT NULL
password_hash: TEXT NOT NULL
created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
updated_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
```

### Table: tasks
Application-specific tasks table

```
id: SERIAL (PRIMARY KEY)
user_id: UUID NOT NULL REFERENCES users(id)
title: VARCHAR(200) NOT NULL
description: TEXT NULL
completed: BOOLEAN NOT NULL DEFAULT FALSE
created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
updated_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
```

## Indexes

### Required Indexes
- `tasks.user_id` - For filtering tasks by user (critical for data isolation)
- `tasks.completed` - For filtering by completion status
- `tasks.created_at` - For sorting tasks chronologically

### Additional Indexes (optional)
- Composite index on `(user_id, completed)` - For combined filtering by user and status

## State Transitions

### Task State Transitions
- `pending` ↔ `completed` (via toggle operation)
  - When `completed` field is updated, `updated_at` automatically updates

## API Data Structures

### Request Models

#### Task Creation Request
```
{
  "title": "Required string, 1-200 chars",
  "description"?: "Optional string, max 1000 chars"
}
```

#### Task Update Request
```
{
  "title"?: "Optional string, 1-200 chars",
  "description"?: "Optional string, max 1000 chars"
}
```

#### Task Completion Toggle Request
```
{
  "completed": "Boolean value"
}
```

### Response Models

#### User Response
```
{
  "id": "UUID string",
  "email": "Valid email string",
  "name": "String, 1-100 chars"
}
```

#### Task Response
```
{
  "id": "Integer ID",
  "user_id": "UUID string",
  "title": "String, 1-200 chars",
  "description": "String or null, max 1000 chars",
  "completed": "Boolean",
  "created_at": "ISO datetime string",
  "updated_at": "ISO datetime string"
}
```

#### Task List Response
```
{
  "tasks": [
    // Array of Task Response objects
  ],
  "total_count": "Integer count",
  "page": "Integer page number",
  "limit": "Integer items per page"
}
```