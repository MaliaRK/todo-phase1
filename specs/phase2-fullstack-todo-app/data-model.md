# Data Model: Phase II Full-Stack Todo Web Application with Authentication Extension

## Entity: User

### Fields
- **id** (String): Primary key, unique identifier for the user
- **email** (String, required): User's email address (unique)
- **name** (String, optional): User's display name
- **created_at** (DateTime): Timestamp when the user account was created (auto-generated)
- **updated_at** (DateTime): Timestamp when the user account was last updated (auto-generated)

### Relationships
- One-to-Many with Task (one user has many tasks)

### Validation Rules
- Email must be valid email format
- Email must be unique across all users
- Email is required
- Name can be up to 255 characters if provided

### State Transitions
- New account: created_at timestamp set
- Account updated: updated_at timestamp updated

## Entity: Task

### Fields
- **id** (UUID/Integer): Primary key, unique identifier for the task
- **title** (String, required): Title of the task, maximum 255 characters
- **description** (Text, optional): Detailed description of the task
- **is_completed** (Boolean): Status indicating if the task is completed (default: false)
- **user_id** (String, required): Foreign key linking to User
- **created_at** (DateTime): Timestamp when the task was created (auto-generated)
- **updated_at** (DateTime): Timestamp when the task was last updated (auto-generated)

### Relationships
- Many-to-One with User (many tasks belong to one user)

### Validation Rules
- Title must be present and not empty
- Title must be less than 255 characters
- Description can be up to 10,000 characters if provided
- is_completed defaults to false when creating a new task
- user_id must reference an existing user

### State Transitions
- New task: is_completed = false
- Task marked complete: is_completed = true
- Task marked incomplete: is_completed = false

## Entity: Session

### Fields
- **id** (String): Primary key, unique identifier for the session
- **user_id** (String, required): Foreign key linking to User
- **expires_at** (DateTime): Timestamp when the session expires
- **created_at** (DateTime): Timestamp when the session was created (auto-generated)

### Relationships
- Many-to-One with User (many sessions belong to one user)

### Validation Rules
- user_id must reference an existing user
- expires_at must be in the future

### State Transitions
- New session: created_at timestamp set, expires_at in future
- Session expired: current time > expires_at

## Database Schema Considerations

### Indexes
- Index on Task.created_at for sorting
- Index on Task.is_completed for filtering completed tasks
- Index on Task.user_id for user-specific queries
- Index on User.email for authentication lookups
- Index on Session.expires_at for cleanup operations

### Constraints
- Task title cannot be empty
- Task title length constraint (255 chars)
- User email uniqueness constraint
- Task user_id foreign key constraint to User.id
- Session user_id foreign key constraint to User.id

## API Representation

### Task Resource (Updated)
```
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Optional description",
  "is_completed": false,
  "user_id": "user-id-string",
  "created_at": "2026-01-04T12:00:00Z",
  "updated_at": "2026-01-04T12:00:00Z"
}
```

### User Resource
```
{
  "id": "user-id-string",
  "email": "user@example.com",
  "name": "User Name",
  "created_at": "2026-01-04T12:00:00Z",
  "updated_at": "2026-01-04T12:00:00Z"
}
```

### Task Creation Request (Updated)
```
{
  "title": "Task title",
  "description": "Optional description"
}
```
*Note: user_id is automatically set based on authenticated user*

### Task Update Request (Updated)
```
{
  "title": "Updated title",        // Optional
  "description": "Updated description", // Optional
  "is_completed": true            // Optional
}
```