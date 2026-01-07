# Next.js Security Best Practices

## Input Validation and Sanitization

Always validate and sanitize user inputs, especially for API routes:

```jsx
// pages/api/users.js
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' })
  }

  const { name, email } = req.body

  // Validate inputs
  if (!name || typeof name !== 'string' || name.length > 50) {
    return res.status(400).json({ message: 'Invalid name' })
  }

  if (!email || typeof email !== 'string' || !isValidEmail(email)) {
    return res.status(400).json({ message: 'Invalid email' })
  }

  // Sanitize inputs if needed
  const sanitizedEmail = sanitizeEmail(email)

  // Process the data
  // ...
}

function isValidEmail(email) {
  // Implement email validation logic
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

function sanitizeEmail(email) {
  // Implement email sanitization logic
  return email.trim().toLowerCase()
}
```

## API Route Security

### Rate Limiting
Implement rate limiting to prevent abuse:

```jsx
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // Limit each IP to 100 requests per windowMs
})

export default async function handler(req, res) {
  // Apply rate limiting
  await new Promise((resolve, reject) =>
    limiter(req, res, (err) => {
      if (err) reject(err)
      else resolve()
    })
  )

  // Your API logic here
}
```

### CORS Configuration
Properly configure CORS for API routes:

```jsx
// pages/api/cors-example.js
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', 'https://yourdomain.com')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization')

  if (req.method === 'OPTIONS') {
    return res.status(200).end()
  }

  // Your API logic here
}
```

## Environment Variables

Use environment variables for sensitive data:

```javascript
// next.config.js
module.exports = {
  env: {
    API_URL: process.env.API_URL,
    SECRET_KEY: process.env.SECRET_KEY
  }
}
```

```jsx
// components/ApiComponent.js
const API_URL = process.env.API_URL

async function fetchData() {
  const response = await fetch(`${API_URL}/data`, {
    headers: {
      'Authorization': `Bearer ${process.env.SECRET_KEY}`
    }
  })
  return response.json()
}
```

## Authentication and Authorization

### Server-Side Authentication
```jsx
// pages/profile.js
export async function getServerSideProps({ req, res }) {
  // Check for authentication token in cookies
  const token = req.cookies.token

  if (!token) {
    return {
      redirect: {
        destination: '/login',
        permanent: false
      }
    }
  }

  // Verify token and fetch user data
  const user = await verifyToken(token)

  if (!user) {
    return {
      redirect: {
        destination: '/login',
        permanent: false
      }
    }
  }

  return {
    props: {
      user
    }
  }
}
```

### Client-Side Authentication
```jsx
// hooks/useAuth.js
import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'

export default function useAuth() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')

    if (!token) {
      setLoading(false)
      return
    }

    // Verify token and set user
    verifyToken(token)
      .then(userData => {
        setUser(userData)
      })
      .catch(() => {
        localStorage.removeItem('token')
        router.push('/login')
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  return { user, loading }
}
```

## Image Security

Always use Next.js Image component for security:

```jsx
import Image from 'next/image'

// Safe image rendering
function MyComponent() {
  return (
    <Image
      src="/path/to/image.jpg"
      alt="Description"
      width={500}
      height={300}
      // For remote images, use the unoptimized prop or add to domains in next.config.js
    />
  )
}
```

## Content Security Policy (CSP)

Implement Content Security Policy headers:

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.google-analytics.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;"
          }
        ]
      }
    ]
  }
}
```

## Security Headers

Add security headers to protect against common vulnerabilities:

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin'
          },
          {
            key: 'Permissions-Policy',
            value: 'geolocation=(), microphone=(), camera=()'
          }
        ]
      }
    ]
  }
}
```