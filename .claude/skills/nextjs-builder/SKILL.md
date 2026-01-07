---
name: nextjs-builder
description: |
  This skill should be used when users need to create Next.js artifacts including components, pages, API routes, and configurations.
  It provides guidance on Next.js best practices, file structure, and implementation patterns for production-ready applications.
---

# Next.js Builder Skill

Build production-ready Next.js artifacts with proper patterns, best practices, and security considerations.

## When to Use This Skill

Use this skill when users need to create:
- Next.js page components with proper routing
- API routes with validation and error handling
- React components with Next.js-specific patterns
- Configuration files (next.config.js, etc.)
- Data fetching implementations
- Image optimization components
- SEO and meta tag implementations

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing Next.js structure, routing patterns, component conventions, and configuration files |
| **Conversation** | User's specific requirements, page types, data needs, styling preferences |
| **Skill References** | Next.js patterns from `references/` (routing, data fetching, optimization) |
| **User Guidelines** | Project-specific conventions, team standards, and existing patterns |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (Next.js expertise is in this skill).

## Core Next.js Concepts

### File-Based Routing
- Pages in `pages/` directory automatically become routes
- Dynamic routes use `[param]` syntax
- Catch-all routes use `[...param]` syntax
- Nested routes created with folder structure

### Data Fetching Methods
- `getStaticProps`: For static generation at build time
- `getStaticPaths`: For dynamic static routes
- `getServerSideProps`: For server-side rendering
- SWR or React Query: For client-side data fetching

### Image Optimization
- Use `next/image` for optimized images
- Always specify `width` and `height` for layout stability
- Use `layout="responsive"` for responsive images

## Implementation Patterns

### Page Creation Pattern
```
1. Identify route structure and URL parameters
2. Create page component with proper TypeScript interfaces
3. Implement appropriate data fetching method
4. Add error handling and loading states
5. Include SEO meta tags with next/head
6. Add proper TypeScript types
```

### Component Creation Pattern
```
1. Determine if component is client or server component
2. Create component with proper TypeScript interfaces
3. Add necessary props validation
4. Include proper accessibility attributes
5. Follow Next.js styling conventions
6. Add proper TypeScript types
```

### API Route Creation Pattern
```
1. Create file in `pages/api/` directory
2. Implement proper request/response handling
3. Add input validation and sanitization
4. Include error handling with appropriate status codes
5. Add rate limiting if needed
6. Follow security best practices
```

## Quality Standards

### Performance
- Use dynamic imports for code splitting
- Optimize images with next/image
- Implement proper caching strategies
- Minimize bundle size

### Security
- Sanitize all user inputs
- Validate API route parameters
- Implement proper authentication
- Use HTTPS in production

### SEO
- Include proper meta tags with next/head
- Use semantic HTML elements
- Implement proper heading hierarchy
- Add structured data where appropriate

## Next.js Best Practices

### File Organization
- Group related files in directories
- Use consistent naming conventions
- Separate components from pages
- Organize API routes logically

### Error Handling
- Create custom error pages (404, 500)
- Implement proper error boundaries
- Use try/catch blocks in API routes
- Provide user-friendly error messages

### TypeScript Integration
- Use strict TypeScript settings
- Create proper interface definitions
- Type all props and state
- Use utility types where appropriate

## Common Next.js Patterns

### Layout Pattern
```jsx
// components/Layout.js
export default function Layout({ children }) {
  return (
    <>
      <Header />
      <main>{children}</main>
      <Footer />
    </>
  )
}
```

### Higher-Order Component Pattern
```jsx
// components/withAuth.js
export default function withAuth(Component) {
  return function AuthenticatedComponent(props) {
    // Authentication logic
    return <Component {...props} />
  }
}
```

### Custom Hook Pattern
```jsx
// hooks/useUser.js
import { useState, useEffect } from 'react'

export default function useUser() {
  const [user, setUser] = useState(null)

  useEffect(() => {
    // Fetch user logic
  }, [])

  return { user }
}
```

## Checklist for Next.js Artifacts

### Pages
- [ ] Proper TypeScript interfaces
- [ ] Appropriate data fetching method implemented
- [ ] Error handling and loading states
- [ ] SEO meta tags with next/head
- [ ] Responsive design considerations
- [ ] Accessibility attributes

### Components
- [ ] Proper TypeScript interfaces
- [ ] Props validation
- [ ] Accessibility attributes
- [ ] Responsive design considerations
- [ ] Proper styling approach
- [ ] Performance optimization

### API Routes
- [ ] Input validation and sanitization
- [ ] Error handling with status codes
- [ ] Rate limiting implementation
- [ ] Security headers
- [ ] Proper CORS configuration
- [ ] Authentication checks

## Troubleshooting Common Issues

### Build Errors
- Ensure all dependencies are properly installed
- Check TypeScript compilation errors
- Verify image paths and dimensions
- Confirm environment variables are set

### Performance Issues
- Check for unnecessary re-renders
- Verify proper code splitting implementation
- Optimize image loading
- Review bundle analyzer output

### Routing Issues
- Verify file naming conventions
- Check dynamic route parameters
- Confirm catch-all route implementation
- Validate nested route structure