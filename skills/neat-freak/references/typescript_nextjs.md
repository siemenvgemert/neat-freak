# TypeScript & Web Architecture Blueprint

Choose between a single-file static application or Next.js App Router based on simplicity requirements.

---

## 1. Low / Clean Tiers (Recommended for simple frontend widgets / single pages)

### Folder Structure
```text
{{project_name}}/
├── .gitignore
├── index.html
├── README.md
└── scratch/                # Sandbox for experimental code (gitignored)
```

### Template Files

#### `index.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{project_name}}</title>
  <style>
    /* ponytail: embedded styling to avoid importing tailwind or extra files for simple layouts */
    body {
      margin: 0;
      font-family: system-ui, -apple-system, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      background: #fafafa;
      color: #171717;
    }
    main {
      padding: 2rem;
      border-radius: 8px;
      background: #ffffff;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
  </style>
</head>
<body>
  <main>
    <h1>Welcome to {{project_name}}</h1>
    <p>This is a native single-page HTML layout with no building steps or external dependencies.</p>
  </main>
  <script>
    // ponytail: native client-side logic in tag to avoid compilation and module setup overhead
    console.log("{{project_name}} initialized successfully!");
  </script>
</body>
</html>
```

---

## 2. Full OCD Tier (For rich web applications using Next.js App Router)

### Folder Structure
```text
{{project_name}}/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── api/
│   │       └── health/
│   │           └── route.ts
│   ├── components/
│   │   └── ui/
│   ├── lib/
│   │   └── utils.ts
│   └── styles/
│       └── globals.css
├── public/
├── .gitignore
├── next.config.js
├── package.json
├── tsconfig.json
├── README.md
└── scratch/                # Sandbox for experimental code (gitignored)
```

### Template Files

#### `package.json`
```json
{
  "name": "{{project_name}}",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next": "^14.1.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.11.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "eslint": "^8.56.0",
    "eslint-config-next": "^14.1.0"
  }
}
```

#### `tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

#### `next.config.js`
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

module.exports = nextConfig;
```

#### `src/app/layout.tsx`
```tsx
import type { Metadata } from "next";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "{{project_name}}",
  description: "Created using neat-freak",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

#### `src/app/page.tsx`
```tsx
export default function Home() {
  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Welcome to {{project_name}}</h1>
      <p>Your scaffolding was generated successfully!</p>
    </main>
  );
}
```

#### `src/app/api/health/route.ts`
```typescript
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ status: "ok", timestamp: new Date().toISOString() });
}
```

#### `src/styles/globals.css`
```css
html,
body {
  padding: 0;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen,
    Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
}
```

---

## 3. General Configurations

### `.gitignore`
```text
/node_modules
/.pnp
.pnp.js
/coverage
/.next/
/out/
/build
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.env*.local
.vercel
*.tsbuildinfo
next-env.d.ts
/scratch/
```
