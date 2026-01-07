# Next.js Routing Guide

## File-Based Routing System

Next.js uses a file-based routing system where each file in the `pages` directory becomes a route in your application.

### Basic Routes
- `pages/index.js` → `/`
- `pages/about.js` → `/about`
- `pages/products.js` → `/products`

### Dynamic Routes
- `pages/posts/[id].js` → `/posts/1`, `/posts/2`, etc.
- `pages/authors/[author]/[post].js` → `/authors/john/first-post`, etc.

### Catch-All Routes
- `pages/blog/[...slug].js` → `/blog/`, `/blog/a`, `/blog/a/b`, etc.

### Optional Catch-All Routes
- `pages/blog/[[...slug]].js` → Matches `/blog`, `/blog/a`, `/blog/a/b`, etc.

## Linking Between Pages

Use the `next/link` component for client-side navigation:

```jsx
import Link from 'next/link'

function Home() {
  return (
    <div>
      <Link href="/about">
        <a>About Us</a>
      </Link>
    </div>
  )
}
```

## Programmatic Navigation

Use the `next/router` for programmatic navigation:

```jsx
import { useRouter } from 'next/router'

function MyComponent() {
  const router = useRouter()

  const handleClick = () => {
    router.push('/about')
  }

  return <button onClick={handleClick}>Go to About</button>
}
```