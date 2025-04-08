#!/bin/bash

# Development Environment Setup Script

echo "Setting up development environment..."

# Check for required tools
echo "Checking for required tools..."
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed. Aborting." >&2; exit 1; }

# Create project structure
echo "Creating project structure..."
mkdir -p packages/{backend,frontend}
mkdir -p packages/backend/{app,models,services,routes,tests}
mkdir -p packages/frontend/{src,public,components,hooks,utils,tests}

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set up Node.js environment
echo "Setting up Node.js environment..."
cd packages/frontend
npm init -y
npm install next@latest react@latest react-dom@latest typescript@latest @types/react@latest @types/node@latest
npm install --save-dev eslint prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Create TypeScript configuration
echo "Creating TypeScript configuration..."
cat > tsconfig.json << EOF
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
EOF

# Create ESLint configuration
echo "Creating ESLint configuration..."
cat > .eslintrc.json << EOF
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/explicit-module-boundary-types": "off",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "error"
  }
}
EOF

# Create Prettier configuration
echo "Creating Prettier configuration..."
cat > .prettierrc << EOF
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
EOF

# Create Next.js configuration
echo "Creating Next.js configuration..."
cat > next.config.js << EOF
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
EOF

# Create environment example files
echo "Creating environment example files..."
cd ../backend
cat > .env.example << EOF
# Security
JWT_SECRET=your_jwt_secret
REFRESH_TOKEN_SECRET=your_refresh_token_secret
ENCRYPTION_KEY=your_encryption_key

# Database
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_NAME=mindscape
DB_HOST=localhost
DB_PORT=5432

# API
API_PORT=8000
API_HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
EOF

cd ../frontend
cat > .env.example << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
EOF

# Create initial README files
echo "Creating README files..."
cd ../backend
cat > README.md << EOF
# Mindscape Backend

## Setup
1. Create a virtual environment: \`python -m venv venv\`
2. Activate the virtual environment: \`source venv/bin/activate\`
3. Install dependencies: \`pip install -r requirements.txt\`
4. Copy \`.env.example\` to \`.env\` and configure
5. Run migrations: \`alembic upgrade head\`
6. Start the server: \`uvicorn app.main:app --reload\`

## Development
- API documentation: http://localhost:8000/docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
EOF

cd ../frontend
cat > README.md << EOF
# Mindscape Frontend

## Setup
1. Install dependencies: \`npm install\`
2. Copy \`.env.example\` to \`.env\` and configure
3. Start the development server: \`npm run dev\`

## Development
- Development server: http://localhost:3000
- API endpoint: http://localhost:8000
EOF

echo "Development environment setup complete!" 