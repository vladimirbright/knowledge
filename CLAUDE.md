# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based knowledge management system (Russian: "база знаний") that allows users to create, organize, and share code snippets and technical notes. The application uses PostgreSQL as the database and supports BBCode formatting for code highlighting.

## Development Commands

### Environment Setup
```bash
# Install dependencies using uv
uv sync

# Install development dependencies
uv sync --group dev

# Activate virtual environment
source .venv/bin/activate

# Or run commands directly with uv
uv run python manage.py runserver
```

### Running the Application
```bash
# Start Django development server
uv run python manage.py runserver

# Collect static files
uv run python manage.py collectstatic

# Run database migrations
uv run python manage.py migrate
```

### Database Management
```bash
# Create new migrations
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate

# Access Django shell
uv run python manage.py shell
```

### Package Management
```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --group dev package-name

# Remove a dependency
uv remove package-name

# Update dependencies
uv sync

# Show installed packages
uv tree
```

### Production Deployment
```bash
# Deploy using Fabric (requires proper SSH setup)
fab deploy

# Individual deployment steps
fab git_pull
fab collect_static
fab migrate
fab restart
```

## Architecture

### Core Django Apps

- **cards/**: Main application managing knowledge cards (code snippets/notes)
  - `Cards` model: Stores individual knowledge entries with BBCode support
  - `Category` and `Tag` models: Hierarchical organization system
  - `CardFavorites`: User bookmarking system
  - `CardsImage`: Image attachments for cards

- **users/**: User management and profiles
- **feeds/**: RSS feed generation
- **sitemap/**: XML sitemap generation for SEO

### Key Models Structure

- `Category` → `Tag` → `Cards` (hierarchical organization)
- `User` → `Cards` (ownership relationship)
- `User` → `CardFavorites` → `Cards` (bookmarking system)

### Database Configuration

- **Engine**: PostgreSQL with psycopg2
- **Database**: `knowledgedb`
- **User**: `knowledge`
- Settings include Russian localization (ru-RU)

### Static Files

- **Development**: Assets stored in `/assets/` directory
- **Production**: Static files collected to `/s/` directory
- Blueprint CSS framework for styling
- jQuery and MarkItUp editor for rich text editing

### Key Features

- BBCode parsing and syntax highlighting for code snippets
- User authentication and authorization
- Favorites/bookmarking system with rating
- Category and tag-based organization
- Search functionality
- RSS feeds
- Image attachments
- Responsive design with Blueprint CSS

### Template Structure

- Base template: `templates/base.html`
- Card detail view: `templates/cards/cards_detail.html`
- Main listing: `templates/index.html`
- User authentication: `templates/registration/`

### Dependencies

Key packages managed by uv in `pyproject.toml`:
- Django 4.2+ (modern Django version)
- Pillow (Python Imaging Library)
- Pygments (syntax highlighting)
- psycopg2-binary (PostgreSQL adapter)
- django-pagination
- django-disqus (comments)
- bbcode (BBCode parsing)
- easy-thumbnails (image processing)
- fabric (deployment automation)

Development dependencies:
- black (code formatting)
- flake8 (linting)
- isort (import sorting)
- pre-commit (git hooks)
- django-debug-toolbar (debugging)
- django-extensions (additional commands)
- ipython (enhanced shell)

## Development Notes

- **Modernized Django project**: Upgraded from Django 1.x to Django 4.2+
- **Python 3**: Updated from Python 2.6 to Python 3.8+
- **Modern package management**: Uses uv instead of pip for dependency management
- **Built-in migrations**: Uses Django's built-in migration system (South removed)
- **Modern URL routing**: Updated to use `path()` instead of `url()` patterns
- **Russian interface and content**: Maintains original Russian localization
- **Production deployment**: Uses Fabric for automation
- **Database**: Contains sensitive information (password in settings.py) - consider using environment variables

## Package Management with uv

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management:

- **pyproject.toml**: Modern Python project configuration
- **uv.lock**: Deterministic dependency resolution
- **Virtual environment**: Automatically managed in `.venv/`
- **Fast installs**: Significantly faster than pip
- **Dependency groups**: Separate dev dependencies from production