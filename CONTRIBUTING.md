# Contributing to DACP

Thank you for your interest in contributing to DACP! This document provides guidelines and information for contributors.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/dacp.git
   cd dacp
   ```
3. Install in development mode:
   ```bash
   pip install -e .[dev]
   ```

## Development Workflow

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run tests and linting:
   ```bash
   make all
   ```
4. Commit your changes with a descriptive message
5. Push to your fork and create a pull request

## Code Style

- Use **Black** for code formatting
- Use **Flake8** for linting
- Use **MyPy** for type checking
- Follow PEP 8 guidelines
- Write docstrings for all public functions and classes

## Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting a PR
- Aim for high test coverage
- Use pytest for testing

## Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run linting
make lint

# Format code
make format
```

## Pull Request Guidelines

1. **Title**: Use a clear, descriptive title
2. **Description**: Explain what the PR does and why
3. **Tests**: Include tests for new functionality
4. **Documentation**: Update documentation if needed
5. **Type Hints**: Add type hints to new functions
6. **Breaking Changes**: Clearly document any breaking changes

## Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a release tag
4. GitHub Actions will automatically publish to PyPI

## Questions?

If you have questions about contributing, please open an issue or reach out to the maintainers.

Thank you for contributing to DACP! 