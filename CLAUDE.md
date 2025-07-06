# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based knowledge management system (Russian: "база знаний") that allows users to create, organize, and share code snippets and technical notes. The application uses PostgreSQL as the database and supports BBCode formatting for code highlighting.

## Development Commands

### Running the Application
```bash
# Start Django development server
python3 manage.py runserver

# Collect static files
python3 manage.py collectstatic

# Run database migrations
python3 manage.py migrate
```

### Database Management
```bash
# Create new migrations
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate

# Access Django shell
python3 manage.py shell
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

### Third-party Dependencies

Key packages from `pip.req.txt`:
- Django (older version, likely 1.x)
- PIL (Python Imaging Library)
- Pygments (syntax highlighting)
- South (database migrations)
- psycopg2 (PostgreSQL adapter)
- django-pagination
- django-disqus (comments)

## Development Notes

- This is a legacy Django project using older conventions (Django 1.x era)
- Uses South for migrations instead of Django's built-in system
- Python 2.6 shebang in manage.py indicates older Python version
- Russian interface and content
- Production deployment uses Fabric for automation
- Database contains sensitive information (password in settings.py)