# Quickstart Guide: Chatbot Assessment Interface

**Date**: 2025-10-25  
**Feature**: 003-chatbot-assessment-interface  
**Purpose**: Get the chatbot assessment platform running locally for development

## Prerequisites

### System Requirements

- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **PostgreSQL**: 15 or higher
- **Redis**: 6 or higher
- **Git**: Latest version
- **Docker**: Optional, for containerized deployment

### Development Tools

- **Code Editor**: VS Code, PyCharm, or similar
- **API Testing**: Postman, Insomnia, or curl
- **Database Client**: pgAdmin, DBeaver, or psql
- **Redis Client**: RedisInsight or redis-cli

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

# Install Rasa dependencies
cd chatbot
pip install -r requirements.txt
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
createdb myway_chatbot_assessment

# Run database migrations
cd backend
python manage.py migrate
cd ..
```

### 3. Redis Setup

```bash
# Start Redis service
# On macOS with Homebrew:
brew services start redis

# On Ubuntu/Debian:
sudo systemctl start redis

# Test Redis connection
redis-cli ping
```

### 4. Environment Configuration

Create `.env` files for backend, frontend, and chatbot:

**Backend `.env`:**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/myway_chatbot_assessment
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000
RASA_SERVER_URL=http://localhost:5005
```

**Frontend `.env`:**
```env
REACT_APP_API_URL=http://localhost:8000/v1
REACT_APP_WEBSOCKET_URL=ws://localhost:8000/ws
REACT_APP_ENVIRONMENT=development
```

**Chatbot `.env`:**
```env
RASA_SERVER_URL=http://localhost:5005
RASA_ACTION_SERVER_URL=http://localhost:5055
```

### 5. Start Development Servers

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

**Terminal 3 - Rasa Server:**
```bash
cd chatbot
rasa run --enable-api --cors "*" --port 5005
```

**Terminal 4 - Rasa Action Server:**
```bash
cd chatbot
rasa run actions --port 5055
```

### 6. Verify Installation

- **Backend API**: http://localhost:8000/docs (Swagger UI)
- **Frontend App**: http://localhost:3000
- **Rasa Server**: http://localhost:5005
- **Database**: Connect to `myway_chatbot_assessment` database
- **Redis**: Connect to Redis on port 6379

## Chatbot Training

### 1. Train Rasa Model

```bash
cd chatbot
rasa train
```

### 2. Test Chatbot

```bash
# Interactive testing
rasa shell

# Test specific intents
rasa test
```

### 3. Load Assessment Questions

```bash
cd backend
python scripts/load_questions.py
```

## API Testing

### 1. Start Chatbot Session

```bash
curl -X POST "http://localhost:8000/v1/chatbot/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "initial_message": "Xin chào, tôi muốn làm bài đánh giá nghề nghiệp"
  }'
```

### 2. Send Message to Chatbot

```bash
curl -X POST "http://localhost:8000/v1/chatbot/sessions/{session_id}/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Tôi muốn bắt đầu làm bài đánh giá",
    "message_type": "text"
  }'
```

### 3. Start Assessment

```bash
curl -X POST "http://localhost:8000/v1/assessments/start" \
  -H "Content-Type: application/json" \
  -d '{
    "chatbot_session_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
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

### 3. Load Chatbot Training Data

```bash
cd chatbot
python scripts/load_training_data.py
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

**Chatbot Tests:**
```bash
cd chatbot
rasa test
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

**Chatbot:**
```bash
cd chatbot
rasa test
rasa data validate
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
      POSTGRES_DB: myway_chatbot_assessment
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/myway_chatbot_assessment
      REDIS_URL: redis://redis:6379
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000/v1
      REACT_APP_WEBSOCKET_URL: ws://localhost:8000/ws

  rasa:
    build: ./chatbot
    ports:
      - "5005:5005"
    environment:
      RASA_SERVER_URL: http://localhost:5005
    depends_on:
      - backend

volumes:
  postgres_data:
```

### 2. Start with Docker

```bash
docker-compose up -d
```

## WebSocket Testing

### 1. Connect to WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chatbot/{session_id}');

ws.onopen = function(event) {
    console.log('Connected to chatbot WebSocket');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

ws.onclose = function(event) {
    console.log('Disconnected from chatbot WebSocket');
};
```

### 2. Send Message via WebSocket

```javascript
ws.send(JSON.stringify({
    type: 'message',
    content: 'Xin chào, tôi muốn làm bài đánh giá',
    session_id: 'your-session-id'
}));
```

## Production Deployment

### 1. Environment Variables

Set production environment variables:

```env
# Production .env
DATABASE_URL=postgresql://user:pass@prod-db:5432/myway_chatbot_assessment
REDIS_URL=redis://prod-redis:6379
SECRET_KEY=production-secret-key
JWT_SECRET_KEY=production-jwt-secret
CORS_ORIGINS=https://myway.vn
RASA_SERVER_URL=https://chatbot.myway.vn
```

### 2. Database Setup

```bash
# Create production database
createdb myway_chatbot_assessment_prod

# Run migrations
python manage.py migrate --settings=config.production
```

### 3. Rasa Model Deployment

```bash
cd chatbot
rasa train
# Deploy model to production server
```

## Troubleshooting

### Common Issues

**1. Database Connection Error**
```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Check database exists
psql -l | grep myway_chatbot_assessment
```

**2. Redis Connection Error**
```bash
# Check Redis is running
brew services list | grep redis

# Test Redis connection
redis-cli ping
```

**3. Rasa Server Error**
```bash
# Check Rasa model is trained
cd chatbot
rasa test

# Check Rasa server logs
rasa run --enable-api --verbose
```

**4. WebSocket Connection Error**
```bash
# Check WebSocket endpoint
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Sec-WebSocket-Key: test" -H "Sec-WebSocket-Version: 13" http://localhost:8000/ws/chatbot/test
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

**Chatbot Logs:**
```bash
# Enable Rasa debug mode
rasa run --enable-api --debug
```

**Database Logs:**
```bash
# Check PostgreSQL logs
tail -f /usr/local/var/log/postgresql.log
```

**Redis Logs:**
```bash
# Check Redis logs
redis-cli monitor
```

## Next Steps

1. **Complete Chatbot Flow**: Test the full user journey from chatbot interaction to results
2. **Add Test Data**: Create comprehensive test datasets for development
3. **Performance Testing**: Load test with concurrent users
4. **Security Review**: Audit authentication and data protection
5. **UI/UX Testing**: Validate interface with target demographic (students aged 15-25)

## Support

- **Documentation**: Check `/docs` endpoint for API documentation
- **Issues**: Report bugs in the project repository
- **Development**: Follow the development guidelines in the project README
