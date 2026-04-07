# PixelDex Pro

A hybrid Pokémon and Cobblemon platform featuring an interactive Pokédex, battle analysis tools, Cobblemon spawn finder, Pokémon comparator, and team builder/analyzer.

## Features

- **Pokédex** - Complete Pokémon database with detailed stats, abilities, and evolutions
- **Battle Analysis** - Type effectiveness calculator with weakness/resistance charts
- **Cobblemon Spawn Finder** - Search and filter spawn locations for Cobblemon mod
- **Pokémon Compare** - Side-by-side comparison of stats, types, and spawn locations
- **Team Builder** - Build and analyze teams with type coverage insights
- **Favorites** - Save and organize your favorite Pokémon

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Zustand (state management)
- React Query (data fetching)
- React Router (routing)

### Backend
- Python 3.11+
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Alembic (migrations)
- Pydantic (validation)

### Database
- PostgreSQL 15+
- Redis (optional, for caching)

## Project Structure

```
PixelDexPro/
├── backend/
│   ├── main.py              # FastAPI application entry
│   ├── requirements.txt     # Python dependencies
│   ├── alembic/             # Database migrations
│   ├── api/routes/          # API endpoints
│   ├── core/                # Configuration
│   ├── db/                  # Database session
│   ├── integrations/        # External API clients
│   ├── models/              # SQLAlchemy models
│   ├── repositories/        # Data access layer
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── hooks/           # Custom hooks
│   │   ├── pages/           # Page components
│   │   ├── services/        # API clients
│   │   ├── store/           # Zustand stores
│   │   ├── types/           # TypeScript types
│   │   └── utils/           # Utility functions
│   ├── index.html
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/yourusername/PixelDexPro.git
cd PixelDexPro

# Copy environment variables
cp .env.example .env

# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp ../.env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Database Setup

```bash
# Create PostgreSQL database
createdb pixeldex

# Or using psql
psql -U postgres -c "CREATE DATABASE pixeldex;"
```

## API Endpoints

### Pokémon
- `GET /api/v1/pokemon` - List all Pokémon (with pagination)
- `GET /api/v1/pokemon/{id}` - Get Pokémon by ID
- `GET /api/v1/pokemon/{id}/details` - Get detailed Pokémon info
- `GET /api/v1/pokemon/search` - Search Pokémon by name

### Types
- `GET /api/v1/types` - List all types
- `GET /api/v1/types/chart` - Get type effectiveness chart

### Cobblemon
- `GET /api/v1/cobblemon/spawns` - List spawns (with filters)
- `GET /api/v1/cobblemon/spawns/{pokemon_id}` - Get spawns by Pokémon
- `GET /api/v1/cobblemon/biomes` - List all biomes

### Compare
- `GET /api/v1/compare` - Compare two Pokémon

### Teams
- `POST /api/v1/teams` - Create a team
- `GET /api/v1/teams/{id}` - Get team by ID
- `POST /api/v1/teams/{id}/pokemon` - Add Pokémon to team
- `GET /api/v1/teams/{id}/analysis` - Analyze team composition

### Favorites
- `GET /api/v1/favorites` - List favorites
- `POST /api/v1/favorites/{pokemon_id}` - Add to favorites
- `DELETE /api/v1/favorites/{pokemon_id}` - Remove from favorites

### Sync (Data Import)
- `POST /api/v1/sync/pokeapi/pokemon` - Sync Pokémon from PokéAPI
- `POST /api/v1/sync/pokeapi/types` - Sync types from PokéAPI
- `POST /api/v1/sync/cobblemon/spawns` - Import Cobblemon spawn data

## Data Sources

- **Pokémon Data**: [PokéAPI](https://pokeapi.co/) - RESTful Pokémon API
- **Cobblemon Spawns**: Cobblemon Wiki / Google Sheets

## Configuration

See `.env.example` for all available configuration options:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/pixeldex` |
| `POKEAPI_BASE_URL` | PokéAPI base URL | `https://pokeapi.co/api/v2` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `JWT_SECRET_KEY` | JWT signing key | (required for auth) |

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Style

```bash
# Backend - format with black
black backend/

# Frontend - format with prettier
cd frontend && npm run format
```

### Database Migrations

```bash
cd backend

# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PokéAPI](https://pokeapi.co/) for the comprehensive Pokémon data
- [Cobblemon](https://cobblemon.com/) for the Minecraft mod inspiration
- [Tailwind CSS](https://tailwindcss.com/) for the styling system
