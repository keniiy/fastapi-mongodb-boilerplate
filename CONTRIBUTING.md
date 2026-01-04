# Contributing Guide

Thank you for considering contributing to this project! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or 3.12
- Poetry (package manager)
- Git
- MongoDB 7+ (or use Docker)
- Basic understanding of Clean Architecture principles

### Setup

1. **Fork the repository** and clone your fork:
   ```bash
   git clone https://github.com/your-username/test-app.git
   cd test-app
   ```

2. **Install dependencies**:
   ```bash
   poetry install --with dev
   ```

3. **Install pre-commit hooks**:
   ```bash
   poetry run pre-commit install
   ```

4. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Workflow

### Code Style

This project uses automated code formatting and linting. **Always run these before committing:**

```bash
# Format code
make format

# Or manually:
poetry run black app tests
poetry run isort app tests
poetry run ruff format app tests

# Check linting
make lint

# Or manually:
poetry run ruff check app tests
```

### Pre-commit Hooks

Pre-commit hooks automatically run on `git commit`. They check:
- Code formatting (Black, isort, Ruff)
- Linting (Ruff)
- Type checking (MyPy)
- Security issues (Bandit)
- File integrity (YAML, JSON, TOML)

**If hooks fail**, fix the issues and commit again. You can skip hooks with `--no-verify` (not recommended).

### Writing Code

1. **Follow Clean Architecture**:
   - Domain layer: Pure business logic, no framework dependencies
   - Infrastructure layer: External concerns (DB, APIs, etc.)
   - Presentation layer: FastAPI-specific code

2. **Write Type Hints**:
   ```python
   async def get_user(user_id: str) -> Optional[User]:
       ...
   ```

3. **Add Docstrings**:
   ```python
   def create_user(email: str, password: str) -> User:
       """
       Create a new user.

       Args:
           email: User email address
           password: Plain text password (will be hashed)

       Returns:
           Created User entity

       Raises:
           ValidationError: If email is invalid
           ConflictError: If user already exists
       """
   ```

### Testing

**Always write tests** for new features:

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
poetry run pytest tests/test_auth.py -v
```

**Test Requirements:**
- MongoDB must be running (use Docker: `make docker-up`)
- Tests should be independent (use fixtures for setup/teardown)
- Aim for >70% code coverage

### MongoDB Considerations

- **IDs**: Use `str` type for IDs (ObjectId strings)
- **Models**: Use Pydantic models instead of SQLAlchemy ORM
- **Indexes**: Add index creation in `init_db()` function
- **Queries**: Use MongoDB query syntax instead of SQL

### Submitting Changes

1. **Ensure all tests pass**:
   ```bash
   make test
   ```

2. **Ensure code quality checks pass**:
   ```bash
   make lint
   make format-check
   ```

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature"  # Use conventional commits
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

Example:
```
feat: add user profile update endpoint

- Add PATCH /api/v1/auth/me endpoint
- Add UpdateProfileUseCase
- Add tests for profile update
```

## 📋 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] All tests pass (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] Linting passes (`make lint`)
- [ ] Type checking passes (`make type-check`)
- [ ] Documentation is updated (if needed)
- [ ] Commit messages follow conventional commits
- [ ] PR description is clear and detailed

## 🐛 Reporting Bugs

If you find a bug:

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)
   - Relevant logs/error messages

## 💡 Suggesting Features

Feature suggestions are welcome! Please:

1. **Check existing issues** first
2. **Create a feature request** with:
   - Clear description
   - Use case / motivation
   - Proposed implementation (if applicable)

## 📚 Resources

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Motor Documentation](https://motor.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

Thank you for contributing! 🎉

