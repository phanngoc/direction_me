#!/bin/bash

# MyWay Development Runner
# Script để chạy toàn bộ backend + frontend cho development

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to kill process on port
kill_port() {
    if port_in_use $1; then
        print_warning "Port $1 is in use, killing existing process..."
        lsof -ti :$1 | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

# Function to setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    cd ..
    print_success "Backend setup completed!"
}

# Function to setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_status "Installing Node.js dependencies..."
        if command_exists yarn; then
            yarn install
        else
            npm install
        fi
    fi
    
    cd ..
    print_success "Frontend setup completed!"
}

# Function to start database services
start_services() {
    print_status "Starting database services (PostgreSQL & Redis)..."
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    # Stop any existing containers to avoid conflicts
    print_status "Cleaning up existing containers..."
    docker-compose down 2>/dev/null || true
    
    # Kill any processes using our ports
    kill_port 5455
    kill_port 6380
    
    # Start only database services
    docker-compose up -d db redis
    
    # Wait for services to be ready
    print_status "Waiting for database services to be ready..."
    sleep 10
    
    # Check if services are healthy
    if docker-compose ps db | grep -q "healthy"; then
        print_success "PostgreSQL is ready!"
    else
        print_warning "PostgreSQL might not be fully ready yet..."
    fi
    
    if docker-compose ps redis | grep -q "healthy"; then
        print_success "Redis is ready!"
    else
        print_warning "Redis might not be fully ready yet..."
    fi
}

# Function to start backend
start_backend() {
    print_status "Starting backend server..."
    
    # Kill any existing process on port 8000
    kill_port 8000
    
    cd backend
    source venv/bin/activate
    
    # Set environment variables
    export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5455/myway_assessment"
    export REDIS_URL="redis://localhost:6380"
    export SECRET_KEY="dev-secret-key"
    export JWT_SECRET_KEY="dev-jwt-secret"
    export CORS_ORIGINS="http://localhost:3000"
    
    # Start FastAPI server
    print_status "Starting FastAPI server on http://localhost:8000"
    uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    
    cd ..
    
    # Wait a moment for backend to start
    sleep 3
    
    if port_in_use 8000; then
        print_success "Backend server started successfully!"
    else
        print_error "Failed to start backend server"
        return 1
    fi
}

# Function to start frontend
start_frontend() {
    print_status "Starting frontend server..."
    
    # Kill any existing process on port 3000
    kill_port 3000
    
    cd frontend
    
    # Set environment variables
    export NEXT_PUBLIC_API_URL="http://localhost:8000"
    export NEXT_PUBLIC_WEBSOCKET_URL="ws://localhost:8000/ws"
    export NEXT_PUBLIC_ENVIRONMENT="development"
    
    # Start Next.js development server
    print_status "Starting Next.js server on http://localhost:3000"
    if command_exists yarn; then
        yarn dev &
    else
        npm run dev &
    fi
    FRONTEND_PID=$!
    
    cd ..
    
    # Wait a moment for frontend to start
    sleep 5
    
    if port_in_use 3000; then
        print_success "Frontend server started successfully!"
    else
        print_error "Failed to start frontend server"
        return 1
    fi
}

# Function to show running services
show_services() {
    echo ""
    print_success "=== Development Environment Ready! ==="
    echo ""
    echo "🚀 Services running:"
    echo "   • Frontend (Next.js):  http://localhost:3000"
    echo "   • Backend (FastAPI):   http://localhost:8000"
    echo "   • API Documentation:   http://localhost:8000/docs"
    echo "   • PostgreSQL:          localhost:5455"
    echo "   • Redis:               localhost:6380"
    echo ""
    echo "📝 Logs:"
    echo "   • Backend logs: Check terminal output"
    echo "   • Frontend logs: Check terminal output"
    echo "   • Database logs: docker-compose logs db"
    echo ""
    echo "🛑 To stop all services: Ctrl+C or run './run.sh stop'"
    echo ""
}

# Function to stop all services
stop_services() {
    print_status "Stopping all services..."
    
    # Kill backend and frontend processes
    kill_port 8000
    kill_port 3000
    
    # Stop Docker services
    docker-compose down
    
    print_success "All services stopped!"
}

# Function to show help
show_help() {
    echo "MyWay Development Runner"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start     Start all services (default)"
    echo "  stop      Stop all services"
    echo "  restart   Restart all services"
    echo "  setup     Setup dependencies only"
    echo "  backend   Start only backend services"
    echo "  frontend  Start only frontend"
    echo "  services  Start only database services"
    echo "  status    Show running services"
    echo "  help      Show this help message"
    echo ""
}

# Function to check status
check_status() {
    echo "Service Status:"
    echo ""
    
    if port_in_use 3000; then
        print_success "✓ Frontend (port 3000): Running"
    else
        print_error "✗ Frontend (port 3000): Not running"
    fi
    
    if port_in_use 8000; then
        print_success "✓ Backend (port 8000): Running"
    else
        print_error "✗ Backend (port 8000): Not running"
    fi
    
    if port_in_use 5455; then
        print_success "✓ PostgreSQL (port 5455): Running"
    else
        print_error "✗ PostgreSQL (port 5455): Not running"
    fi
    
    if docker-compose ps redis 2>/dev/null | grep -q "Up"; then
        print_success "✓ Redis: Running"
    else
        print_error "✗ Redis: Not running"
    fi
}

# Main execution
main() {
    case "${1:-start}" in
        "start")
            print_status "Starting MyWay development environment..."
            setup_backend
            setup_frontend
            start_services
            start_backend
            start_frontend
            show_services
            
            # Keep script running and wait for Ctrl+C
            trap 'stop_services; exit 0' INT
            print_status "Press Ctrl+C to stop all services..."
            wait
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            stop_services
            sleep 2
            main start
            ;;
        "setup")
            setup_backend
            setup_frontend
            print_success "Setup completed!"
            ;;
        "backend")
            setup_backend
            start_services
            start_backend
            print_success "Backend services started!"
            trap 'stop_services; exit 0' INT
            wait
            ;;
        "frontend")
            setup_frontend
            start_frontend
            print_success "Frontend started!"
            trap 'kill_port 3000; exit 0' INT
            wait
            ;;
        "services")
            start_services
            print_success "Database services started!"
            ;;
        "status")
            check_status
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Check prerequisites
check_prerequisites() {
    local missing_deps=()
    
    if ! command_exists python3; then
        missing_deps+=("python3")
    fi
    
    if ! command_exists node; then
        missing_deps+=("node")
    fi
    
    if ! command_exists docker; then
        missing_deps+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        echo "Please install the missing dependencies and try again."
        exit 1
    fi
}

# Run prerequisite check
check_prerequisites

# Execute main function
main "$@"