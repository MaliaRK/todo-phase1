# Next.js Performance Optimization

## Image Optimization

Always use the `next/image` component for optimized images:

```jsx
import Image from 'next/image'

function MyComponent() {
  return (
    <Image
      src="/images/my-image.jpg"
      alt="Description"
      width={500}
      height={300}
      // Optional: layout for responsive images
      layout="responsive"
    />
  )
}
```

For remote images, configure in `next.config.js`:

```javascript
// next.config.js
module.exports = {
  images: {
    domains: ['example.com', 'cdn.example.com'],
    // Or use remotePatterns for more control (Next.js 12+)
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        port: '',
        pathname: '/images/**',
      },
    ],
  }
}
```

## Code Splitting

### Dynamic Imports
Split code using dynamic imports:

```jsx
import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'

// Dynamically import heavy components
const HeavyComponent = dynamic(() => import('../components/HeavyComponent'))

// With loading component
const ComponentWithLoader = dynamic(
  () => import('../components/Component'),
  {
    loading: () => <p>Loading...</p>
  }
)

// Import specific functions from libraries
const { chart } = await import('chart.js')
```

### Route-Based Code Splitting
Each page is automatically code-split by Next.js, but you can optimize further:

```jsx
// pages/dashboard.js
import dynamic from 'next/dynamic'

// Dynamically import dashboard sections
const AnalyticsSection = dynamic(() => import('../sections/Analytics'))
const ReportsSection = dynamic(() => import('../sections/Reports'))

export default function Dashboard() {
  return (
    <div>
      <AnalyticsSection />
      <ReportsSection />
    </div>
  )
}
```

## Bundle Analysis

Analyze your bundle to identify large dependencies:

```bash
npm run build
# Next.js will automatically show bundle analyzer information
```

Or use a dedicated tool:

```bash
npm install @next/bundle-analyzer
```

## Font Optimization

Use Next.js built-in font optimization:

```jsx
// pages/_document.js
import Document, { Html, Head, Main, NextScript } from 'next/document'

class MyDocument extends Document {
  render() {
    return (
      <Html>
        <Head>
          <link rel="preconnect" href="https://fonts.googleapis.com" />
          <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="true" />
          <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet" />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default MyDocument
```

Or use the built-in Font component (Next.js 12+):

```jsx
// pages/_app.js
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function App({ Component, pageProps }) {
  return (
    <main className={inter.className}>
      <Component {...pageProps} />
    </main>
  )
}
```

## Preloading and Prefetching

### Link Prefetching
Next.js automatically prefetches visible links in the viewport:

```jsx
import Link from 'next/link'

function Navigation() {
  return (
    <nav>
      {/* This link will be prefetched */}
      <Link href="/about">About</Link>
    </nav>
  )
}
```

### Programmatic Prefetching
Prefetch pages programmatically:

```jsx
import { useRouter } from 'next/router'

function MyComponent() {
  const router = useRouter()

  useEffect(() => {
    // Prefetch the about page
    router.prefetch('/about')
  }, [router])

  return (
    <button onClick={() => router.push('/about')}>
      Go to About
    </button>
  )
}
```

## Caching Strategies

### Static Generation with Revalidation
Use ISR for content that updates periodically:

```jsx
// pages/products.js
export async function getStaticProps() {
  const products = await fetchProducts()

  return {
    props: {
      products
    },
    // Revalidate every 60 seconds
    revalidate: 60
  }
}
```

### Client-Side Caching
Use SWR for client-side data caching:

```jsx
import useSWR from 'swr'

const fetcher = (url) => fetch(url).then((res) => res.json())

function ProductList() {
  const { data, error } = useSWR('/api/products', fetcher, {
    // Cache for 60 seconds
    dedupingInterval: 60000,
    // Refresh when window is focused
    refreshWhenHidden: false
  })

  if (error) return <div>Failed to load</div>
  if (!data) return <div>Loading...</div>

  return (
    <div>
      {data.products.map(product => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  )
}
```

## Optimizing API Routes

### Response Caching
Add caching headers to API routes:

```jsx
// pages/api/products.js
export default async function handler(req, res) {
  // Enable response caching
  res.setHeader(
    'Cache-Control',
    'public, s-maxage=10, stale-while-revalidate=59'
  )

  const products = await fetchProducts()

  res.json(products)
}
```

### Database Connection Pooling
Reuse database connections:

```jsx
// lib/db.js
let client

export async function connectToDatabase() {
  if (!client) {
    client = new MongoClient(process.env.MONGODB_URI)
    await client.connect()
  }

  const db = client.db(process.env.DB_NAME)
  return { client, db }
}
```

## Component Optimization

### Memoization
Use React.memo to prevent unnecessary re-renders:

```jsx
import { memo } from 'react'

const ExpensiveComponent = memo(({ items }) => {
  return (
    <div>
      {items.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  )
})

// Custom comparison function
const CustomMemoComponent = memo(({ a, b }) => {
  return <div>{a} {b}</div>
}, (prevProps, nextProps) => {
  return prevProps.a === nextProps.a && prevProps.b === nextProps.b
})
```

### Use useMemo and useCallback
Optimize expensive calculations and prevent function recreation:

```jsx
import { useMemo, useCallback } from 'react'

function MyComponent({ items, onItemClick }) {
  // Memoize expensive calculations
  const expensiveValue = useMemo(() => {
    return items.reduce((acc, item) => acc + item.value, 0)
  }, [items])

  // Memoize callback functions
  const handleClick = useCallback((id) => {
    onItemClick(id)
  }, [onItemClick])

  return (
    <div>
      <p>Total: {expensiveValue}</p>
      {items.map(item => (
        <button key={item.id} onClick={() => handleClick(item.id)}>
          {item.name}
        </button>
      ))}
    </div>
  )
}
```