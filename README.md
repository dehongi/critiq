# Critiq - Movie Review Platform

Critiq is a Django-based web application for sharing and discovering movie reviews. Users can create an account, add movies to the platform, write detailed reviews with ratings, and explore reviews from other users.

## Features

- **User Authentication**: Custom email-based authentication system with password reset functionality
- **Movie Management**: Add, edit, and delete movies with details like title, director, release year, and synopsis
- **Movie Posters**: Upload and display poster images for movies
- **Review System**: Write detailed reviews for movies with ratings (1-10 scale)
- **User Reviews**: View all reviews written by a specific user
- **Search Functionality**: Search for movies across the platform
- **Responsive Design**: Mobile-friendly interface with a clean base template
- **Information Pages**: About, FAQ, Help, Contact, Privacy Policy, and Terms of Service pages

## Tech Stack

- **Backend**: Django 5.1.7
- **Database**: SQLite3
- **Frontend**: HTML/CSS templates with Django template engine
- **Image Handling**: Pillow for image processing
- **Python Version**: 3.x

## Project Structure

```
critiq/
├── accounts/              # User authentication and account management
│   ├── models.py         # Custom user model with email authentication
│   ├── views.py          # Login, signup, password reset views
│   ├── forms.py          # User registration and login forms
│   └── urls.py           # Account URL routing
│
├── critiq/               # Main movie review application
│   ├── models.py         # Movie and Review models
│   ├── views.py          # CRUD views for movies and reviews
│   ├── forms.py          # Movie and review forms
│   ├── urls.py           # Movie review URL routing
│   └── migrations/       # Database migration files
│
├── website/              # Static website pages
│   ├── views.py          # Views for about, help, contact, etc.
│   └── urls.py           # Website URL routing
│
├── django_project/       # Django project configuration
│   ├── settings.py       # Project settings and app configuration
│   ├── urls.py           # Main URL routing
│   ├── asgi.py           # ASGI configuration
│   └── wsgi.py           # WSGI configuration
│
├── templates/            # HTML templates for all apps
│   ├── base.html         # Base template with navigation
│   ├── accounts/         # User authentication templates
│   ├── critiq/           # Movie and review templates
│   └── website/          # Static page templates
│
├── requirements.txt      # Python dependencies
├── manage.py             # Django management script
└── db.sqlite3           # SQLite database file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd critiq
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**

   ```bash
   python manage.py runserver
   ```

The application will be available at `http://localhost:8000/`

## Usage

### Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` using your superuser credentials to manage users, movies, and reviews directly.

### User Features

1. **Sign Up**: Create a new account using an email address
2. **Login**: Access your account with your credentials
3. **Add Movies**: Contribute movies to the platform with details and posters
4. **Write Reviews**: Rate and review movies you've watched (one review per user per movie)
5. **Browse Movies**: Search and discover movies on the platform
6. **View Reviews**: See reviews from other users for each movie
7. **Manage Your Content**: Edit or delete your own movies and reviews

## Models

### Custom User Model (accounts.models)

- Email-based authentication
- Supports custom user attributes
- Password reset functionality

### Movie Model (critiq.models)

- Title, slug, release year, director
- Synopsis and poster image
- User-created (foreign key to User)
- Automatic slug generation with UUID collision handling
- Calculated average rating from reviews

### Review Model (critiq.models)

- Title and content with slug
- Rating (1-10 scale)
- Foreign key to Movie and User
- Ensures one review per user per movie
- Automatic slug generation

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 5.1.7 | Web framework |
| Pillow | 11.1.0 | Image processing |
| asgiref | 3.8.1 | Django ASGI utilities |
| sqlparse | 0.5.3 | SQL parsing |

## Database Schema

The application uses SQLite3 with the following main tables:

- `auth_user` / Custom user table - User accounts
- `critiq_movie` - Movie information
- `critiq_review` - User reviews with ratings
- Django's standard tables for authentication and sessions

## Configuration

### Important Settings (django_project/settings.py)

- **DEBUG**: Currently set to `True` (change to `False` in production)
- **ALLOWED_HOSTS**: Empty by default (configure for production)
- **SECRET_KEY**: Should be changed in production
- **DATABASES**: SQLite3 configuration
- **INSTALLED_APPS**:
  - `accounts` - User authentication
  - `critiq` - Core application
  - `website` - Static pages

## URL Routing

- `/accounts/` - User authentication routes
- `/critiq/` - Movie and review management routes
- `/website/` - Static page routes
- `/admin/` - Django admin panel

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Loading Static Files

```bash
python manage.py collectstatic
```

## Security Notes

⚠️ **Important for Production Deployment**:

1. Change `DEBUG` to `False`
2. Change `SECRET_KEY` to a secure value
3. Configure `ALLOWED_HOSTS` with actual domain names
4. Use environment variables for sensitive settings
5. Use PostgreSQL or MySQL instead of SQLite
6. Set `CSRF_TRUSTED_ORIGINS` appropriately
7. Enable HTTPS and set `SECURE_SSL_REDIRECT = True`
8. Set secure cookie flags

## License

[Add appropriate license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues, questions, or suggestions, please [create an issue](link-to-issue-tracker) or contact the project maintainers.
