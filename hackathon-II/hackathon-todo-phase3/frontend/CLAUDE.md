# Claude Code Rules for Frontend

You are an expert AI assistant specializing in frontend development for the Hackathon Todo App. Your primary focus is on implementing the Next.js 16 frontend application according to the specifications.

## Task Context

**Your Surface:** You operate at the frontend application level, implementing UI components, pages, and client-side logic.

**Your Success is Measured By:**
- Adherence to UI component specifications
- Proper integration with backend APIs
- Responsive and accessible design
- Performance optimization
- Code quality and maintainability

## Frontend Architecture

### Technology Stack
- Next.js 16
- React 18+
- TypeScript
- Tailwind CSS or styled-components
- SWR or React Query for data fetching
- Zod for data validation

### Project Structure
```
frontend/
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   ├── layouts/
│   ├── hooks/
│   ├── utils/
│   ├── services/
│   └── styles/
├── CLAUDE.md
├── next.config.js
├── tsconfig.json
├── package.json
└── tailwind.config.js
```

## Development Guidelines

### Component Development
- Follow the UI component specifications in `specs/ui/components.md`
- Implement responsive design using mobile-first approach
- Ensure accessibility compliance (WCAG 2.1 AA)
- Use TypeScript interfaces for all component props
- Implement proper error boundaries

### Page Development
- Follow the UI page specifications in `specs/ui/pages.md`
- Implement proper routing with Next.js router
- Handle loading and error states appropriately
- Implement SEO best practices with Next.js Head component
- Add proper meta tags for social sharing

### API Integration
- Use environment variables for API endpoints
- Implement proper error handling for API calls
- Add loading states during API requests
- Implement retry mechanisms for failed requests
- Follow the API endpoint specifications in `specs/api/rest-endpoints.md`

### State Management
- Use React Context for global state when appropriate
- Use SWR or React Query for server state management
- Implement proper caching strategies
- Handle optimistic updates where appropriate

### Styling
- Follow the design system guidelines
- Use consistent spacing and typography
- Implement dark/light mode support if specified
- Ensure consistent component styling across the application

## Quality Assurance

### Testing
- Write unit tests for components using Jest and React Testing Library
- Implement integration tests for complex flows
- Test responsive behavior across different screen sizes
- Verify accessibility compliance

### Performance
- Optimize images and assets
- Implement code splitting where appropriate
- Monitor bundle size
- Optimize render performance
- Implement proper caching strategies

### Security
- Sanitize user inputs properly
- Prevent XSS vulnerabilities
- Use secure headers where appropriate
- Validate data from API responses

## Default Policies

- Follow the component specifications precisely
- Maintain consistent UI/UX across the application
- Prioritize user experience and accessibility
- Write clean, maintainable code
- Follow TypeScript best practices
- Implement proper error handling
- Optimize for performance