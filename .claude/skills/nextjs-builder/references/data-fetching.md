# Next.js Data Fetching Guide

## Server-Side Rendering (SSR)

Use `getServerSideProps` when you need to render a page at request time:

```jsx
export async function getServerSideProps(context) {
  const res = await fetch(`https://api.example.com/posts`)
  const posts = await res.json()

  return {
    props: {
      posts
    }
  }
}

export default function Posts({ posts }) {
  return (
    <div>
      {posts.map((post) => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  )
}
```

## Static Site Generation (SSG)

Use `getStaticProps` for pre-rendering at build time:

```jsx
export async function getStaticProps() {
  const res = await fetch('https://api.example.com/posts')
  const posts = await res.json()

  return {
    props: {
      posts
    },
    revalidate: 60, // Re-generate page every 60 seconds
  }
}

export default function Posts({ posts }) {
  // Component implementation
}
```

## Dynamic SSG with getStaticPaths

For dynamic routes with static generation:

```jsx
// pages/posts/[id].js
export async function getStaticProps({ params }) {
  const res = await fetch(`https://api.example.com/posts/${params.id}`)
  const post = await res.json()

  return {
    props: {
      post
    },
    revalidate: 60
  }
}

export async function getStaticPaths() {
  const res = await fetch('https://api.example.com/posts')
  const posts = await res.json()

  const paths = posts.map((post) => ({
    params: { id: post.id.toString() }
  }))

  return {
    paths,
    fallback: 'blocking' // or 'true' or 'false'
  }
}

export default function Post({ post }) {
  // Component implementation
}
```

## Client-Side Data Fetching

For user-specific content or real-time data:

```jsx
import { useState, useEffect } from 'react'
import useSWR from 'swr'

const fetcher = (url) => fetch(url).then((res) => res.json())

function Profile() {
  const { data, error } = useSWR('/api/user', fetcher)

  if (error) return <div>Failed to load</div>
  if (!data) return <div>Loading...</div>

  return <div>Hello {data.name}!</div>
}
```

## Incremental Static Regeneration (ISR)

Update static content after build without rebuilding the entire site:

```jsx
export async function getStaticProps() {
  const res = await fetch('https://api.example.com/products')
  const products = await res.json()

  return {
    props: {
      products
    },
    revalidate: 3600, // Re-generate page every hour
  }
}
```