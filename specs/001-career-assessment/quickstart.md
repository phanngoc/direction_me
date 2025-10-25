# Quickstart Guide: MyWay Career Assessment System

**Date**: 2024-12-19  
**Feature**: 001-career-assessment  
**Purpose**: Get the system running quickly for development and testing

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git

## Quick Setup (5 minutes)

### 1. Clone and Setup Backend

```bash
# Clone repository
git clone <repository-url>
cd direction_me

# Setup Python environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb myway_assessment
python scripts/init_db.py

# Run migrations
python scripts/migrate.py

# Start backend server
python -m uvicorn src.main:app --reload --port 8000
```

### 2. Setup Frontend

```bash
# In new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Verify Installation

- Backend: http://localhost:8000/docs (FastAPI docs)
- Frontend: http://localhost:3000
- Database: Check with `psql myway_assessment`

## Development Workflow

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

### Database Operations

```bash
# Create migration
python scripts/create_migration.py "add_new_field"

# Apply migrations
python scripts/migrate.py

# Reset database (development only)
python scripts/reset_db.py
```

### Algorithm Testing

```bash
# Test assessment algorithms
cd backend
python -m algorithms.test_iq_scoring
python -m algorithms.test_ikigai_calculation
python -m algorithms.test_career_mapping

# CLI interface for algorithms
python -m algorithms.cli --help
```

## API Testing

### Using curl

```bash
# Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123", "full_name": "Test User", "age": 20}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Start assessment
curl -X POST http://localhost:8000/assessments \
  -H "Authorization: Bearer <token>"
```

### Using FastAPI Docs

1. Go to http://localhost:8000/docs
2. Click "Authorize" and enter your JWT token
3. Test endpoints directly in the browser

## Configuration

### Environment Variables

Create `.env` files:

**Backend (.env)**:
```env
DATABASE_URL=postgresql://user:password@localhost/myway_assessment
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=MyWay Assessment
```

### Database Configuration

**PostgreSQL Setup**:
```sql
-- Create database
CREATE DATABASE myway_assessment;

-- Create user (optional)
CREATE USER myway_user WITH PASSWORD 'myway_pass';
GRANT ALL PRIVILEGES ON DATABASE myway_assessment TO myway_user;
```

## Sample Data

### Load Test Data

```bash
# Load sample questions
python scripts/load_sample_questions.py

# Load career rules
python scripts/load_career_rules.py

# Create test users
python scripts/create_test_users.py
```

### Sample Assessment Flow

1. **Register**: POST `/auth/register`
2. **Login**: POST `/auth/login`
3. **Start Assessment**: POST `/assessments`
4. **Get Questions**: GET `/assessments/{id}/questions?category=IQ`
5. **Submit Answers**: POST `/assessments/{id}/answers`
6. **Complete Assessment**: POST `/assessments/{id}/complete`
7. **Get Results**: GET `/results/{id}`
8. **Get Career Suggestions**: GET `/results/{id}/careers`
9. **Get Learning Path**: GET `/results/{id}/learning-path`

## Troubleshooting

### Common Issues

**Database Connection Error**:
```bash
# Check PostgreSQL is running
pg_ctl status

# Check connection
psql -h localhost -U myway_user -d myway_assessment
```

**Port Already in Use**:
```bash
# Find process using port
lsof -i :8000
lsof -i :3000

# Kill process
kill -9 <PID>
```

**Module Import Errors**:
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Logs and Debugging

**Backend Logs**:
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python -m uvicorn src.main:app --reload --log-level debug
```

**Frontend Logs**:
```bash
# Enable verbose logging
npm run dev -- --verbose
```

**Database Logs**:
```bash
# Enable PostgreSQL logging
# Edit postgresql.conf: log_statement = 'all'
# Restart PostgreSQL
```

## Performance Testing

### Load Testing

```bash
# Install artillery
npm install -g artillery

# Run load test
artillery run tests/load-test.yml
```

### Database Performance

```bash
# Check slow queries
psql myway_assessment -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"

# Analyze query plans
psql myway_assessment -c "EXPLAIN ANALYZE SELECT * FROM assessment_results WHERE user_id = 'uuid';"
```

## Deployment

### Docker Setup

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Production Checklist

- [ ] HTTPS enabled
- [ ] Database backups configured
- [ ] Environment variables set
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Monitoring setup
- [ ] Error tracking configured

## Next Steps

1. **Read the full documentation**: Check `docs/` directory
2. **Explore the codebase**: Start with `backend/src/algorithms/`
3. **Run the test suite**: Ensure all tests pass
4. **Try the assessment**: Complete a full assessment flow
5. **Check the API**: Explore endpoints in FastAPI docs

## Getting Help

- **Documentation**: Check `docs/` directory
- **Issues**: Create GitHub issue
- **API Reference**: http://localhost:8000/docs
- **Database Schema**: See `data-model.md`
- **Algorithm Details**: See `research.md`
