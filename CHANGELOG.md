# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- MongoDB database support with Motor (async driver)
- Automatic index creation on startup
- MongoDB connection pooling and health checks
- `.editorconfig` for consistent code formatting across editors
- `CHANGELOG.md` for version tracking
- Environment management commands in Makefile (`make env-*`)

### Changed
- Replaced SQLAlchemy with Motor for MongoDB
- Replaced Pydantic models with SQLAlchemy models
- Changed from integer IDs to string IDs (ObjectId)
- Updated database configuration for MongoDB
- Enhanced health check endpoint with MongoDB connectivity check

### Fixed
- Startup error when `.env` file is missing (now uses sensible defaults)
- Deprecated FastAPI event handler warnings

## [1.0.0] - 2024-12-31

### Added
- Initial FastAPI Clean Architecture boilerplate with MongoDB
- User authentication (register, login, logout, refresh token)
- JWT authentication with access and refresh tokens
- Password hashing with Argon2
- Clean Architecture with Domain-Driven Design
- Repository pattern with adapters
- Global exception handling with structured error responses
- Trace ID middleware for request tracking
- Rate limiting (global and per-endpoint)
- Pre-commit hooks for code quality
- GitHub Actions CI/CD workflows
- Docker and Docker Compose setup
- Comprehensive test suite with pytest
- Code quality tools (Black, isort, Ruff, MyPy, Bandit)
- Makefile with common development commands
- Comprehensive documentation (README, CONTRIBUTING)

[Unreleased]: https://github.com/keniiy/test-app/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/keniiy/test-app/releases/tag/v1.0.0

