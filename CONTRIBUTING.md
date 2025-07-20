# Contributing to EditEngine

Thank you for your interest in contributing to EditEngine! This document provides guidelines for contributing to the project.

**Documentation:** For project overview and features, see [README.md](README.md). For technical architecture details, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributions from developers of all skill levels.

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Use the issue template if available
- Provide clear steps to reproduce bugs
- Include relevant system information and error messages

### Suggesting Features

- Open an issue to discuss new features before implementing
- Explain the use case and expected behavior
- Consider if the feature fits the project's scope

### Development Setup

1. **Prerequisites:**

   - Python 3.10+
   - Node.js 18+
   - PostgreSQL

2. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/yourusername/EditEngine.git
   cd EditEngine
   ```

3. **Set up the development environment:**

   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Set up environment variables
   cp .env.template .env
   # Edit .env file and replace:
   # - SECRET_KEY with a long, random string (e.g., use `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
   # - DB_PASSWORD with your PostgreSQL password
   # - Update other database settings if needed

   # Set up database
   createdb editengine
   python manage.py migrate

   # PostgreSQL is used as the Celery message broker
   ```

4. **Start the development server:**

   **Option 1: Using honcho (recommended for managing multiple processes):**

   ```bash
   # Start all processes with one command
   honcho start -f Procfile.dev
   ```

   This will start both the web server (frontend + backend) and Celery worker in a single terminal.

   **Option 2: Manual approach (separate terminals):**

   ```bash
   # Terminal 1: Start both frontend and backend
   python manage.py dev

   # Terminal 2: Start the worker
   python manage.py celery worker -l info
   ```

### Development Workflow

1. **Create a feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**

   - Follow the existing code style and patterns
   - Add tests for new functionality
   - Update documentation if needed

3. **Run quality checks:**

   ```bash
   # Backend checks (must pass)
   python manage.py lint
   python manage.py test
   python manage.py test:coverage
   ```

   **Testing specific files:**

   ```bash
   # Test specific files by name
   python manage.py test wiki_utils
   python manage.py lint wiki_utils spelling_utils
   python manage.py test:coverage test_wiki_utils

   # Test with pytest arguments
   python manage.py test wiki_utils -v --tb=short
   ```

   **Supported file pattern formats:**

   - Code file names: `wiki_utils`, `wiki_utils.py`
   - Test file names: `test_wiki_utils`, `test_wiki_utils.py`
   - Multiple files: `wiki_utils spelling_utils text_utils`
   - Full paths: `services/utils/wiki_utils.py`

4. **Commit your changes:**

   ```bash
   git add .
   git commit -m "Add feature: description of changes"
   ```

5. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Guidelines

- **Title:** Clear, descriptive title
- **Description:** Explain what changes were made and why
- **Testing:** Describe how you tested the changes
- **Breaking Changes:** Note any breaking changes
- **Screenshots:** Include screenshots for UI changes

### Code Style

**Python:**

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Run `python manage.py lint` before committing

**TypeScript/React:**

- Use TypeScript for all new code
- Follow existing component patterns
- Use SCSS modules for styling
- Avoid inline styles

**Frontend Styling Guidelines:**

- Avoid using values outside of the design system
- Prefer using flex gap where possible. Avoid giving components margins to improve their reusability
- Use SASS nesting where possible
- Do not use shadows, transitions, or animations

**General:**

- Keep functions small and focused
- Use meaningful variable names
- Add comments for complex logic
- No commented-out code in commits

### Testing

- Write unit tests for new functions
- Add integration tests for API endpoints
- Ensure all tests pass before submitting PR
- Maintain or improve test coverage

### Architecture

EditEngine follows a clean three-tier architecture:

- **API Layer** (`api/`): Thin layer handling HTTP requests/responses, authentication, and serialization
- **Services Layer** (`services/`): Fat layer containing all business logic, AI integration, and validation
- **Data Layer** (`data/`): Thin layer for data models, repository patterns, and database access

### Project Structure

```
EditEngine/
├── client/frontend/          # React frontend
│   ├── src/components/       # React components
│   └── src/utils/           # Utilities and API client
├── edit/                    # Django backend
│   ├── api/                 # REST API endpoints
│   ├── services/            # Business logic
│   └── tests/               # Test files
└── manage.py               # Django management
```

### Key Areas for Contribution

- **Frontend Components:** React components in `client/frontend/src/components/`
- **API Endpoints:** Django views in `edit/api/views.py`
- **Edit Services:** Core logic in `edit/services/editing/`
- **Validation:** Quality checks in `edit/services/validation/`
- **Documentation:** Improve setup guides and API docs

### Getting Help

- Open an issue for questions about the codebase
- Check the README.md for setup instructions
- Review existing code for patterns and examples

### Common Issues

- **Database errors:** Ensure PostgreSQL is running and configured correctly
- **PostgreSQL connection:** Ensure PostgreSQL is running and accessible for both data and message broker needs
- **Frontend build:** Use `python manage.py build --frontend-only` for detailed errors
- **Test failures:** Run `python manage.py test` with verbose output

## Release Process

Releases are handled by project maintainers. Contributors should:

1. Target the `main` branch for pull requests
2. Update version numbers in separate commits
3. Add entries to CHANGELOG.md for significant changes

Thank you for contributing to EditEngine!
