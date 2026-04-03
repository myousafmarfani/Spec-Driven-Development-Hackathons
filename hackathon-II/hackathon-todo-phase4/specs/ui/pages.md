# UI Pages Specification

## Page Structure
The application follows a Next.js 16 routing structure with server-side rendering where appropriate.

## Pages

### Public Pages
- **`/` (Home)**: Landing page with app overview and CTA to login/signup
  - Hero section with app benefits
  - Feature highlights
  - Call-to-action buttons

- **`/login`**: User authentication page
  - Login form
  - Link to registration
  - Password recovery option

- **`/register`**: User registration page
  - Registration form
  - Link to login
  - Terms and conditions

- **`/forgot-password`**: Password recovery request
  - Email input form
  - Link back to login

- **`/reset-password/[token]`**: Password reset form
  - New password input
  - Confirmation
  - Token validation

### Protected Pages (require authentication)
- **`/dashboard`**: User dashboard
  - Task overview statistics
  - Recent tasks
  - Quick task creation

- **`/tasks`**: Task management page
  - Task list with filtering/sorting
  - Bulk actions
  - Create task button
  - Pagination

- **`/tasks/[id]`**: Individual task detail page
  - Full task details
  - Activity log
  - Related tasks

- **`/profile`**: User profile management
  - Profile information
  - Account settings
  - Security settings

- **`/settings`**: Application settings
  - Theme preferences
  - Notification settings
  - Privacy settings

## Page Layouts
- **PublicLayout**: Minimal layout for public pages (home, auth)
- **AppLayout**: Full layout with navigation for authenticated users
- **DashboardLayout**: Dashboard-specific layout with widgets

## Page Requirements
- All protected pages must validate authentication token
- Loading states for API requests
- Error boundaries for handling exceptions
- SEO-friendly meta tags
- Responsive design for all screen sizes

## Navigation
- Client-side navigation using Next.js router
- Breadcrumb navigation for deep pages
- Back button support
- Active link highlighting

## Page Transitions
- Smooth transitions between pages
- Loading indicators for route changes
- Error states for failed page loads