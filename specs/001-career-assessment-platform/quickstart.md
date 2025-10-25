# Quickstart Guide: MyWay Career Assessment Platform

**Date**: 2025-10-25  
**Feature**: 001-career-assessment-platform  
**Purpose**: Get the career assessment platform running locally for development

## Prerequisites

### System Requirements

- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **PostgreSQL**: 15 or higher
- **Git**: Latest version
- **Docker**: Optional, for containerized deployment

### Development Tools

- **Code Editor**: VS Code, PyCharm, or similar
- **API Testing**: Postman, Insomnia, or curl
- **Database Client**: pgAdmin, DBeaver, or psql

## Local Development Setup

### 1. Clone and Setup Repository

```bash
# Clone the repository
git clone <repository-url>
cd direction_me

# Create virtual environment for Python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node.js dependencies
cd frontend
npm install
cd ..
```

### 2. Database Setup

```bash
# Start PostgreSQL service
# On macOS with Homebrew:
brew services start postgresql

# On Ubuntu/Debian:
sudo systemctl start postgresql

# Create database
createdb myway_assessment

# Run database migrations
cd backend
python manage.py migrate
cd ..
```

### 3. Environment Configuration

Create `.env` files for both backend and frontend:

**Backend `.env`:**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/myway_assessment
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000
```

**Frontend `.env`:**
```env
REACT_APP_API_URL=http://localhost:8000/v1
REACT_APP_ENVIRONMENT=development
```

### 4. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 5. Verify Installation

- **Backend API**: http://localhost:8000/docs (Swagger UI)
- **Frontend App**: http://localhost:3000
- **Database**: Connect to `myway_assessment` database

## API Testing

### 1. Register a Test User

```bash
curl -X POST "http://localhost:8000/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User",
    "age": 20,
    "education_level": "university",
    "field_of_study": "Computer Science"
  }'
```

### 2. Login and Get Token

```bash
curl -X POST "http://localhost:8000/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### 3. Start Assessment Session

```bash
curl -X POST "http://localhost:8000/v1/assessments/start" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

## Database Seeding

### 1. Load Assessment Questions

```bash
cd backend
python scripts/seed_questions.py
```

### 2. Load Career Database

```bash
python scripts/seed_careers.py
```

### 3. Load Learning Resources

```bash
python scripts/seed_resources.py
```

## Development Workflow

### 1. Running Tests

**Backend Tests:**
```bash
cd backend
pytest tests/ -v
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

**End-to-End Tests:**
```bash
cd frontend
npm run test:e2e
```

### 2. Code Quality Checks

**Backend:**
```bash
cd backend
black src/ tests/
flake8 src/ tests/
mypy src/
```

**Frontend:**
```bash
cd frontend
npm run lint
npm run type-check
```

### 3. Database Migrations

```bash
cd backend
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate <previous_migration>
```

## Docker Development

### 1. Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myway_assessment
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/myway_assessment
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000/v1

volumes:
  postgres_data:
```

### 2. Start with Docker

```bash
docker-compose up -d
```

## Production Deployment

### 1. Environment Variables

Set production environment variables:

```env
# Production .env
DATABASE_URL=postgresql://user:pass@prod-db:5432/myway_assessment
SECRET_KEY=production-secret-key
JWT_SECRET_KEY=production-jwt-secret
CORS_ORIGINS=https://myway.vn
```

### 2. Database Setup

```bash
# Create production database
createdb myway_assessment_prod

# Run migrations
python manage.py migrate --settings=config.production
```

### 3. Static Files

```bash
# Collect static files
python manage.py collectstatic

# Serve with nginx or similar
```

## Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Check database exists
psql -l | grep myway_assessment
```

**2. Port Already in Use**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

**3. Python Dependencies**
```bash
# Reinstall requirements
pip install -r backend/requirements.txt --force-reinstall
```

**4. Node Modules Issues**
```bash
# Clear node modules and reinstall
rm -rf frontend/node_modules
cd frontend
npm install
```

### Logs and Debugging

**Backend Logs:**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python -m uvicorn src.main:app --reload
```

**Frontend Logs:**
```bash
# Enable React debug mode
REACT_APP_DEBUG=true npm start
```

**Database Logs:**
```bash
# Check PostgreSQL logs
tail -f /usr/local/var/log/postgresql.log
```

## Next Steps

1. **Complete Assessment Flow**: Test the full user journey from registration to results
2. **Add Test Data**: Create comprehensive test datasets for development
3. **Performance Testing**: Load test with 500 concurrent users
4. **Security Review**: Audit authentication and data protection
5. **UI/UX Testing**: Validate interface with target demographic (students aged 15-25)

## Support

- **Documentation**: Check `/docs` endpoint for API documentation
- **Issues**: Report bugs in the project repository
- **Development**: Follow the development guidelines in the project README
