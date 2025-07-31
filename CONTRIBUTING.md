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
   - MariaDB
   - Redis

2. **MariaDB Setup on Mac Silicon (M1/M2/M3):**

   ```bash
   # Install MariaDB via Homebrew (optimized for Apple Silicon)
   brew install mariadb
   
   # Start MariaDB service
   brew services start mariadb
   
   # Create database and user
   mysql -u $(whoami) -e "CREATE DATABASE IF NOT EXISTS editengine;"
   mysql -u $(whoami) -e "CREATE USER IF NOT EXISTS 'editengine_user'@'localhost' IDENTIFIED BY 'your_password_here';"
   mysql -u $(whoami) -e "GRANT ALL PRIVILEGES ON editengine.* TO 'editengine_user'@'localhost';"
   mysql -u $(whoami) -e "FLUSH PRIVILEGES;"
   
   # Verify connection (should show list of tables after migration)
   mysql -u editengine_user -p editengine -e "SHOW TABLES;"
   ```

   **Notes for Mac Silicon:**
   - MariaDB 11.8.2+ is recommended for ARM64 compatibility
   - Default connection uses your Mac username if no root password is set
   - If you get access denied errors, try: `sudo mysql_secure_installation`
   - The database user `editengine_user` must match your `.env` configuration

3. **Fork and clone the repository:**

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
   # Edit .env file - see "Environment Variables" section below for details

   # Set up database (ensure MariaDB is configured as described in step 2)
   # Update .env file with your database password before running migration
   python manage.py migrate

   # Install and start Redis locally
   # macOS: brew install redis && brew services start redis
   # Ubuntu: sudo apt-get install redis-server && sudo systemctl start redis
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
   
   # See "Environment Variables" section for performance tuning options
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

## Environment Variables

EditEngine uses environment variables for configuration. All deployment-related variables are **required** and will cause Django to fail on startup if not set. Copy `.env.template` to `.env` and update the values.

### Core Configuration

| Variable | Required | Description | Default | Example |
|----------|----------|-------------|---------|---------|
| `SECRET_KEY` | Yes | Django secret key for cryptographic signing | - | Long random string |
| `DEBUG` | No | Enable Django debug mode (never in production) | False | True |

### Database Configuration

| Variable | Required | Description | Default | Example |
|----------|----------|-------------|---------|---------|
| `DB_NAME` | No | MariaDB database name | editengine | editengine |
| `DB_USER` | No | MariaDB username | editengine_user | editengine_user |
| `DB_PASSWORD` | Yes | MariaDB password | - | strong_password_123 |
| `DB_HOST` | No | MariaDB host | localhost | localhost |
| `DB_PORT` | No | MariaDB port | 3306 | 3306 |
| `DB_CONN_MAX_AGE` | Yes | Database connection lifetime in seconds (0 = close after each request) | - | 300 |

### Redis Configuration (Message Broker)

| Variable | Required | Description | Default | Example |
|----------|----------|-------------|---------|---------|
| `REDIS_HOST` | No | Redis server host | localhost | localhost |
| `REDIS_PORT` | No | Redis server port | 6379 | 6379 |
| `REDIS_DB` | No | Redis database number | 0 | 0 |
| `REDIS_PASSWORD` | No | Redis password (leave empty if none) | - | redis_pass_123 |

### Django Web Server Configuration

| Variable | Required | Description | Default | Example |
|----------|----------|-------------|---------|---------|
| `DJANGO_WORKERS` | Yes | Number of Gunicorn worker processes | - | 2 |
| `DJANGO_MAX_REQUESTS` | Yes | Max requests per worker before restart (prevents memory leaks) | - | 1000 |

**`DJANGO_WORKERS` Guidelines:**
- **What it does:** Controls parallel HTTP request handling processes
- **Resource usage:** Each worker uses ~200-250MB RAM
- **Recommended:** 2-4 workers per CPU core
- **For 0.5 cores:** Use 2 workers

### Celery Background Task Configuration

| Variable | Required | Description | Default | Example |
|----------|----------|-------------|---------|---------|
| `CELERY_WORKER_CONCURRENCY` | Yes | Number of concurrent background task workers | 1 | 1-2 (low-resource) |
| `CELERY_PARAGRAPH_BATCH_SIZE` | Yes | Paragraphs processed per AI API call | 3 | 3-5 |
| `CELERY_WORKER_POOL` | No | Worker pool implementation | eventlet | eventlet, prefork, gevent, solo |
| `CELERY_MAX_TASKS_PER_CHILD` | Yes | Max tasks per worker before recycling | 50 | 50-200 |
| `CELERY_ENCRYPTION_KEY` | Yes | 32-byte key for encrypting API keys in transit | - | (generate with script below) |

**Worker Configuration Guidelines:**

**Default (Conservative for 0.5 cores, 512MB RAM):**
- **`CELERY_WORKER_CONCURRENCY=1`:** Single worker prevents CPU thrashing
- **`CELERY_WORKER_POOL=prefork`:** True process isolation, ~50-100MB per worker
- **`CELERY_MAX_TASKS_PER_CHILD=50`:** Recycle workers after 50 tasks to prevent memory leaks

**Alternative Pool Options:**
- **`prefork` (recommended):** Multiple processes, true parallelism, good isolation
- **`eventlet`:** Single process, I/O concurrency, lowest memory overhead (Python 3.13 compatibility issues)
- **`gevent`:** Similar to eventlet, alternative async implementation
- **`solo`:** Single-threaded, ultra-conservative, no concurrency

**Scaling Up (Multiple cores, more RAM):**
- **2+ cores:** Can use `prefork` with `CELERY_WORKER_CONCURRENCY=2-4`
- **Higher throughput:** Increase `CELERY_MAX_TASKS_PER_CHILD=200` for longer-lived workers
- **High-performance:** Use `prefork` with concurrency matching CPU cores

### Generating Required Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Generate CELERY_ENCRYPTION_KEY (32-byte key)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Environment-Specific Configurations

**Development (`.env`):**
```bash
DEBUG=True
DB_CONN_MAX_AGE=0  # Close connections immediately
DJANGO_WORKERS=2
DJANGO_MAX_REQUESTS=1000
CELERY_WORKER_CONCURRENCY=1    # Conservative default for low-resource
CELERY_WORKER_POOL=prefork     # Process isolation with conservative concurrency
CELERY_PARAGRAPH_BATCH_SIZE=3  # Conservative batch size
CELERY_MAX_TASKS_PER_CHILD=50  # Recycle workers frequently to prevent leaks
```

**Production (`.env.production`):**
```bash
DEBUG=False
DB_CONN_MAX_AGE=300  # Keep connections for 5 minutes
DJANGO_WORKERS=2     # For 0.5 CPU cores
DJANGO_MAX_REQUESTS=1000
CELERY_WORKER_CONCURRENCY=1    # Single worker for 0.5 cores, 512MB
CELERY_WORKER_POOL=prefork     # Process isolation, good stability
CELERY_PARAGRAPH_BATCH_SIZE=3  # Conservative for memory constraints
CELERY_MAX_TASKS_PER_CHILD=50  # Frequent recycling for stability
```

**Testing (`.env.test`):**
```bash
DEBUG=True
DB_CONN_MAX_AGE=0
DJANGO_WORKERS=1
DJANGO_MAX_REQUESTS=100
CELERY_WORKER_CONCURRENCY=1    # Minimal for testing
CELERY_WORKER_POOL=solo        # Single-threaded for predictable tests
CELERY_PARAGRAPH_BATCH_SIZE=2  # Small batches for faster tests
CELERY_MAX_TASKS_PER_CHILD=10  # Frequent recycling for clean test state
```

### Performance Tuning Examples

**High-performance setup (4+ cores, 2GB+ memory):**
```bash
export CELERY_WORKER_CONCURRENCY=4
export CELERY_WORKER_POOL=prefork        # True parallelism
export CELERY_PARAGRAPH_BATCH_SIZE=5
export CELERY_MAX_TASKS_PER_CHILD=200    # Longer-lived workers for throughput
```

**Medium performance (2 cores, 1GB memory):**
```bash
export CELERY_WORKER_CONCURRENCY=2
export CELERY_WORKER_POOL=prefork        # Process isolation
export CELERY_PARAGRAPH_BATCH_SIZE=4
export CELERY_MAX_TASKS_PER_CHILD=100    # Balanced recycling frequency
```

**Ultra-conservative (minimal resources):**
```bash
export CELERY_WORKER_CONCURRENCY=1
export CELERY_WORKER_POOL=solo           # Single-threaded
export CELERY_PARAGRAPH_BATCH_SIZE=2
export CELERY_MAX_TASKS_PER_CHILD=25     # Frequent recycling for stability
```

**Start worker with monitoring:**
```bash
# Basic worker with resource monitoring
python manage.py celery worker -l info

# Override pool type for testing
python manage.py celery worker --pool=eventlet -c 1

# Worker automatically includes resource monitoring
python manage.py celery worker -l info
```

### Common Issues

- **Missing environment variables:** Django will fail on startup if required variables are not set. Check the error message for the specific variable name.
- **Database errors:** Ensure MariaDB is running and `DB_PASSWORD` is set correctly
- **Redis connection:** Ensure Redis is running (default: localhost:6379)
- **Celery encryption:** `CELERY_ENCRYPTION_KEY` must be exactly 32 bytes (use generation script)
- **Frontend build:** Use `python manage.py build --frontend-only` for detailed errors
- **Test failures:** Run `python manage.py test` with verbose output

### MariaDB Troubleshooting on Mac Silicon

**Common connection errors:**

1. **"Can't connect to local server through socket '/tmp/mysql.sock'"**
   ```bash
   # Check if MariaDB is running
   brew services list | grep mariadb
   
   # Start MariaDB if not running
   brew services start mariadb
   ```

2. **"Access denied for user 'editengine_user'@'localhost'"**
   ```bash
   # Verify user exists and has correct password
   mysql -u $(whoami) -e "SELECT User, Host FROM mysql.user WHERE User='editengine_user';"
   
   # Update password if needed
   mysql -u $(whoami) -e "ALTER USER 'editengine_user'@'localhost' IDENTIFIED BY 'your_password_here';"
   
   # Ensure .env file has matching DB_PASSWORD
   ```

3. **"Unknown database 'editengine'"**
   ```bash
   # Create database if it doesn't exist
   mysql -u $(whoami) -e "CREATE DATABASE IF NOT EXISTS editengine;"
   ```

4. **Django migration fails with permission errors**
   ```bash
   # Grant all privileges to user
   mysql -u $(whoami) -e "GRANT ALL PRIVILEGES ON editengine.* TO 'editengine_user'@'localhost';"
   mysql -u $(whoami) -e "FLUSH PRIVILEGES;"
   ```

**Environment file configuration:**
Ensure your `.env` file has the correct MariaDB settings:
```bash
DB_PASSWORD='your_password_here'  # Must match the password you set
DB_HOST=localhost
DB_PORT=3306                      # MariaDB default port (not 5432)
DB_NAME=editengine
DB_USER=editengine_user
```

## Release Process

Releases are handled by project maintainers. Contributors should:

1. Target the `main` branch for pull requests
2. Update version numbers in separate commits
3. Add entries to CHANGELOG.md for significant changes

Thank you for contributing to EditEngine!
