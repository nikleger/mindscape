# Mindscape

A modern mind mapping platform built with Next.js, FastAPI, and PostgreSQL.

## Features

- 🧠 Interactive mind mapping
- 👥 Real-time collaboration
- 📱 Responsive design
- 🔒 Secure authentication
- 📊 Analytics and insights
- 🎨 Customizable templates
- 🔄 Auto-save and versioning
- 📤 Export/Import capabilities

## Tech Stack

- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **Database**: PostgreSQL (Supabase)
- **Authentication**: JWT with refresh tokens
- **Real-time**: WebSocket
- **Testing**: Jest, React Testing Library, pytest
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Docker (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/mindscape.git
   cd mindscape
   ```

2. Install dependencies:
   ```bash
   # Install frontend dependencies
   cd packages/frontend
   npm install

   # Install backend dependencies
   cd ../backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   # Frontend
   cp packages/frontend/.env.example packages/frontend/.env.local

   # Backend
   cp packages/backend/.env.example packages/backend/.env
   ```

4. Start the development servers:
   ```bash
   # Start backend
   cd packages/backend
   ./start-backend.bat

   # Start frontend
   cd ../frontend
   ./start-frontend.bat
   ```

5. Access the application:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## Development

### Project Structure

```
mindscape/
├── packages/
│   ├── frontend/         # Next.js frontend
│   └── backend/          # FastAPI backend
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

### Testing

```bash
# Frontend tests
cd packages/frontend
npm test

# Backend tests
cd packages/backend
pytest
```

### Code Quality

```bash
# Frontend linting
cd packages/frontend
npm run lint

# Backend linting
cd packages/backend
flake8
```

## Deployment

### Production Deployment

1. Build the frontend:
   ```bash
   cd packages/frontend
   npm run build
   ```

2. Deploy the backend:
   ```bash
   cd packages/backend
   ./deploy.sh
   ```

### Environment Variables

Required environment variables for both frontend and backend are documented in their respective `.env.example` files.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security

Please report security vulnerabilities to security@mindscape.io.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email support@mindscape.io or join our [Discord community](https://discord.gg/mindscape).

## Acknowledgments

- [Next.js](https://nextjs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Supabase](https://supabase.com/)
- [Tailwind CSS](https://tailwindcss.com/) 