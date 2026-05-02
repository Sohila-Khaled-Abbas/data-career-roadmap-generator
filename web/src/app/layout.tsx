import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Data & AI Career Roadmap Generator',
  description: 'Generate sequential learning roadmaps bridging the gap between job seekers and market demand.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <main style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
          <header style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '20px', marginBottom: '40px' }}>
            <h1 style={{ color: 'var(--primary)', margin: 0 }}>Career Roadmap Generator</h1>
            <p style={{ color: '#94a3b8', marginTop: '10px' }}>AI-Powered Market Insights & Learning Paths</p>
          </header>
          {children}
        </main>
      </body>
    </html>
  )
}
