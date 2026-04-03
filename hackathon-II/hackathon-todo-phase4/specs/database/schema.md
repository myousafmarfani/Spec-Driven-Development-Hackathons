# Database Schema Specification

## Database: PostgreSQL

## Tables

### users
```sql
id: UUID (PRIMARY KEY, DEFAULT gen_random_uuid())
email: VARCHAR(255) UNIQUE NOT NULL
password_hash: TEXT NOT NULL
name: VARCHAR(255)
is_active: BOOLEAN DEFAULT TRUE
created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
updated_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
```

### tasks
```sql
id: UUID (PRIMARY KEY, DEFAULT gen_random_uuid())
title: VARCHAR(255) NOT NULL
description: TEXT
status: VARCHAR(20) DEFAULT 'todo' CHECK (status IN ('todo', 'in-progress', 'completed'))
priority: VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high'))
due_date: TIMESTAMP WITH TIME ZONE
created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
updated_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
user_id: UUID REFERENCES users(id) ON DELETE CASCADE
```

## Indexes
- users.email (UNIQUE INDEX)
- tasks.user_id (INDEX)
- tasks.status (INDEX)
- tasks.due_date (INDEX)
- tasks.created_at (INDEX)

## Constraints
- tasks.title cannot be empty
- tasks.user_id references valid user
- Cascade delete tasks when user is deleted

## Relationships
- One user to many tasks (user_id foreign key in tasks table)

## Sample Queries
```sql
-- Get all tasks for a user
SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC;

-- Get tasks by status
SELECT * FROM tasks WHERE user_id = $1 AND status = $2;

-- Create a new task
INSERT INTO tasks (title, description, status, priority, due_date, user_id)
VALUES ($1, $2, $3, $4, $5, $6) RETURNING *;
```