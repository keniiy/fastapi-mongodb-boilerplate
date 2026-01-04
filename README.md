# FastAPI MongoDB Clean Architecture Boilerplate

A production-ready FastAPI application template following Clean Architecture principles, Domain-Driven Design (DDD), and industry best practices. This boilerplate provides a solid foundation for building scalable, maintainable APIs with MongoDB.

## 🏗️ Architecture

This project follows **Clean Architecture** with clear separation of concerns:

```bash
┌─────────────────────────────────────────────────────────┐
│              Presentation Layer (FastAPI)               │
│  Routes, Controllers, Request/Response Schemas          │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                 Domain Layer (Business Logic)            │
│  Entities, Use Cases, Domain Services, Interfaces       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│            Infrastructure Layer (External)               │
│  Database, Security, External APIs, Adapters           │
└─────────────────────────────────────────────────────────┘
```

### Key Principles

- **Dependency Inversion**: Domain layer defines interfaces, infrastructure implements them
- **Separation of Concerns**: Each layer has a single, well-defined responsibility
- **Testability**: Business logic is independent of frameworks and databases
- **Maintainability**: Changes in one layer don't cascade to others

## 📁 Project Structure

```bash
app/
├── app.py                      # FastAPI application entry point
│
├── common/                     # Shared utilities across layers
│   ├── enums/                  # Domain enums (UserRole, CourseStatus, etc.)
│   ├── exceptions/             # Custom exception classes
│   ├── schemas/                # Reusable Pydantic schemas
│   └── utils/                  # Utility functions (pagination, etc.)
│
├── core/                       # Core configuration
│   └── config.py               # Application settings (Pydantic Settings)
│
├── domain/                     # Business logic layer (framework-agnostic)
│   └── {domain}/
│       ├── entities/           # Domain entities (pure Python objects)
│       ├── use_cases/          # Business use cases
│       └── types/              # Interfaces/contracts (ABC)
│
├── infrastructure/            # External concerns layer
│   ├── db/                     # Database configuration & models
│   │   ├── base/               # Base model & repository
│   │   └── {domain}/           # Domain-specific models & adapters
│   ├── cache/                  # Redis caching & sessions
│   ├── tasks/                  # Celery background tasks
│   └── security/               # Security utilities (JWT, password hashing)
│
└── presentation/              # API layer (FastAPI-specific)
    ├── {domain}/               # Domain-specific routes
    │   ├── routes.py           # API endpoints (one-liner controllers)
    │   ├── schemas/            # Request/Response models
    │   └── dependencies.py    # Dependency injection
    ├── exceptions.py           # Global exception handlers
    └── middleware/             # Custom middleware (trace ID, rate limiting)
```

## 🚀 Quick Start

### Prerequisites

- **Python** 3.11 or 3.12
- **Poetry** (package manager)
- **MongoDB** 7+ (or use Docker)
- **Docker** (optional, for containerized development)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/fastapi-mongodb-boilerplate.git
cd fastapi-mongodb-boilerplate

# Install all dependencies (including dev tools)
poetry install --with dev

# Install pre-commit hooks
poetry run pre-commit install

# Setup environment file
make env-copy  # Creates .env from .env.example
```

### Configuration

The `.env` file is created automatically. Update it with your values:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE_NAME=app_db
MONGODB_POOL_SIZE=10

# Security
SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=development
DEBUG=true

# Redis (for caching, sessions, rate limiting)
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=10

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_DEFAULT=1000/hour
RATE_LIMIT_STORAGE=memory://  # Use "redis://localhost:6379" in production

# Celery (background tasks)
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# CORS (Cross-Origin Resource Sharing)
# Development: Use "*" to allow all origins
# Production: Specify allowed origins (comma-separated or JSON array)
# CORS_ORIGINS=https://app.example.com,https://www.example.com
CORS_ORIGINS=*
```

### Running the Application

#### Development Mode

```bash
# Start database (optional - app will start without it)
make docker-up

# Start app and open docs automatically in browser
make start

# Or run server only (without opening browser)
make run

# Open docs manually (if server is already running)
make start-docs
```

#### Production Mode

```bash
# Using Docker Compose (recommended)
docker-compose up --build

# Or using Gunicorn directly
gunicorn app.app:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
```

#### Health Check

```bash
curl http://localhost:8000/health
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
poetry run pytest tests/test_auth.py -v
```

**Note**: Tests require MongoDB running. Use Docker for local testing:
```bash
make docker-up  # Starts MongoDB and Redis
make test
```

## 🔍 Code Quality

This project enforces code quality through automated tools and pre-commit hooks.

### Code Quality

```bash
# Format code
make format

# Check code quality
make lint

# Run all checks
make pre-commit
```

**Tools Used:**

- Black, isort, Ruff (formatting & linting)
- MyPy (type checking)
- Bandit (security scanning)
- Pre-commit hooks (automatic on git commit)

## 🐳 Docker

### Development Stack

```bash
# Start only dependencies (MongoDB, Redis)
make docker-up
# or: docker-compose -f docker-compose.dev.yml up -d

# Stop dependencies
make docker-down
```

### Production Stack

The production stack includes:

- **MongoDB**: Database
- **Redis**: Caching, sessions, rate limiting, Celery broker
- **API**: FastAPI application
- **Celery Worker**: Background task processing
- **Celery Beat**: Scheduled task scheduler
- **Flower**: Celery monitoring UI (<http://localhost:5555>)

```bash
# Build and start all services
make docker-up-prod
# or: docker-compose up --build -d

# View logs
make docker-logs-prod

# Stop all services
make docker-down-prod
```

## 🔄 Background Tasks (Celery)

This boilerplate includes Celery for background task processing.

### Running Celery (Development)

```bash
# Start Redis first
make docker-up

# In separate terminals:
make celery        # Start worker
make celery-beat   # Start scheduler (optional)
make celery-flower # Start monitoring UI (optional)
```

### Creating Tasks

```python
# app/infrastructure/tasks/my_tasks.py
from app.infrastructure.tasks.celery_app import celery_app
from app.infrastructure.tasks.base import BaseTask

@celery_app.task(base=BaseTask, bind=True)
def my_background_task(self, user_id: str) -> dict:
    # Long-running operation
    return {"status": "completed", "user_id": user_id}

# Calling the task
my_background_task.delay(user_id="507f1f77bcf86cd799439011")  # Async
my_background_task.apply_async(args=["507f1f77bcf86cd799439011"], countdown=60)  # Delayed
```

### Monitoring

- **Flower UI**: <http://localhost:5555> (when running)
- **Redis CLI**: `make redis-cli`

## 🗄️ Caching (Redis)

Redis is used for:

- **Caching**: Store frequently accessed data
- **Sessions**: User session management
- **Rate Limiting**: Request throttling
- **Celery Broker**: Background task queue

### Using the Cache Service

```python
from app.infrastructure.cache import get_cache_service, cached

# Direct usage
cache = get_cache_service()
await cache.set("user:123", user_data, ttl=3600)
user = await cache.get("user:123")

# Decorator for automatic caching
@cached("user", ttl=3600)
async def get_user(user_id: str) -> User:
    # Expensive operation
    return await repository.get_by_id(user_id)
```

## 🗄️ Database (MongoDB)

This project uses MongoDB with Motor (async MongoDB driver) and Pydantic models.

### Key Features

- **Async Operations**: All database operations are async
- **Pydantic Models**: Type-safe models with validation
- **Repository Pattern**: Clean abstraction over database operations
- **Indexes**: Automatically created on startup
- **Connection Pooling**: Efficient connection management

### Working with Models

```python
from app.infrastructure.db.user.model import User
from app.infrastructure.db.user.repository import UserRepository

# Repository usage
repo = UserRepository()
user = await repo.create(db, User(email="user@example.com", ...))
user = await repo.get_by_id(db, user_id)
users = await repo.get_all(db, skip=0, limit=10)
```

### MongoDB Indexes

Indexes are automatically created on application startup. To add new indexes:

```python
# In app/infrastructure/db/config/database.py init_db()
await db.users.create_index("field_name", unique=True)
```

## 🔐 Authentication & Security

### JWT Authentication

- **Access Tokens**: Short-lived (default: 30 minutes)
- **Refresh Tokens**: Long-lived (default: 7 days)
- **Token Rotation**: Refresh tokens are rotated on use

### Password Hashing

- **Algorithm**: Argon2 (winner of Password Hashing Competition)
- **Automatic Rehashing**: Upgrades hash parameters automatically

### Security Best Practices

- Password hashing with Argon2
- JWT token-based authentication
- Rate limiting (global and per-endpoint)
- CORS configuration
- Input validation with Pydantic
- Structured error responses (no sensitive data leakage)

## 📦 Tech Stack

### Core

- **Framework**: FastAPI 0.115+
- **Database**: MongoDB 7+ with Motor (async driver)
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: Argon2 (argon2-cffi)
- **Validation**: Pydantic v2
- **ASGI Server**: Uvicorn + Gunicorn
- **Package Management**: Poetry

### Development & Quality

- **Testing**: pytest, pytest-asyncio, httpx
- **Code Formatting**: Black, isort, Ruff
- **Type Checking**: MyPy
- **Security**: Bandit
- **Pre-commit Hooks**: pre-commit
- **CI/CD**: GitHub Actions

### Infrastructure

- **Containerization**: Docker + Docker Compose
- **Database**: MongoDB 7+
- **Cache/Sessions**: Redis
- **Background Tasks**: Celery + Redis
- **Task Monitoring**: Flower

## 🔧 Configuration

All configuration is managed through environment variables and Pydantic Settings:

- **Development**: `.env` file (git-ignored)
- **Production**: Environment variables or secrets manager
- **Type-Safe**: Pydantic validates all settings at startup

## 📝 API Documentation

When the server is running, visit:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## 🤝 Contributing

1. Fork and clone the repository
2. Install dependencies: `poetry install --with dev`
3. Install pre-commit hooks: `poetry run pre-commit install`
4. Create a feature branch: `git checkout -b feature/your-feature`
5. Make your changes and write tests
6. Run checks: `make pre-commit && make test`
7. Submit a pull request

All PRs are automatically checked for code quality, tests, and security.

## 📄 License

MIT License - feel free to use this as a starting point for your projects.

---

## Built with ❤️ by Keniiy

