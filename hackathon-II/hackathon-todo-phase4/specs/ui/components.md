# UI Components Specification

## Component Library
The application uses a component-based architecture with reusable UI elements.

## Core Components

### Layout Components
- **AppLayout**: Main layout wrapper with header, sidebar, and content area
- **Header**: Navigation bar with logo, navigation links, and user menu
- **Sidebar**: Collapsible navigation sidebar for mobile/desktop

### Authentication Components
- **LoginForm**: Email/password login form with validation
- **RegisterForm**: User registration form with validation
- **ForgotPasswordForm**: Password reset request form
- **ResetPasswordForm**: New password form with confirmation

### Task Components
- **TaskCard**: Display individual task with title, status, priority, due date
- **TaskList**: Grid/list view of multiple tasks with filtering
- **TaskForm**: Form for creating/updating tasks with all fields
- **TaskFilterBar**: Filtering controls for status, priority, date range
- **TaskStatusBadge**: Visual indicator for task status

### Common Components
- **Button**: Reusable button component with variants (primary, secondary, danger)
- **InputField**: Styled input with validation states
- **TextArea**: Multi-line text input with character count
- **Select**: Dropdown selection component
- **Modal**: Overlay modal dialog component
- **Alert**: Notification messages (success, error, warning, info)
- **LoadingSpinner**: Visual loading indicator
- **EmptyState**: Placeholder for empty lists/data

## Component Props Interface

### TaskCard Props
```typescript
interface TaskCardProps {
  task: Task;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: string) => void;
  onChangeStatus?: (taskId: string, status: TaskStatus) => void;
}
```

### TaskForm Props
```typescript
interface TaskFormProps {
  task?: Partial<Task>;
  onSubmit: (taskData: TaskFormData) => void;
  onCancel?: () => void;
  submitText?: string;
}
```

## Styling Approach
- CSS Modules or styled-components for scoped styling
- Theme-based design system with color palette, typography scale, spacing units
- Responsive design with mobile-first approach
- Accessibility compliance (WCAG 2.1 AA)