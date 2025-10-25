# Research Findings: MyWay Career Assessment System

**Date**: 2024-12-19  
**Feature**: 001-career-assessment  
**Purpose**: Resolve technical unknowns and establish best practices

## Assessment Algorithm Implementation

**Decision**: Implement mathematical assessment algorithms as standalone Python libraries

**Rationale**: 
- Core algorithms (IQ, EQ, DQ, AQ, Ikigai) are complex mathematical operations
- Need to be independently testable and reusable
- Should be callable via CLI for testing and validation
- Library-first approach aligns with constitution requirements

**Alternatives considered**:
- Inline implementation in FastAPI services (rejected: harder to test)
- External microservice (rejected: overkill for MVP)

## Career Mapping Strategy

**Decision**: Rule-based career mapping with JSON configuration

**Rationale**:
- 8 predefined careers with weights, thresholds, and bonus keys
- JSON-configurable for A/B testing and market adaptation
- Explainable AI: Shows which facets contributed to high scores
- Simple to implement and maintain

**Alternatives considered**:
- Machine learning model (rejected: requires training data, complex)
- Static hardcoded rules (rejected: not flexible for A/B testing)

## Database Design

**Decision**: PostgreSQL with normalized schema for user data and assessment results

**Rationale**:
- Relational database fits structured assessment data
- ACID compliance for user data integrity
- JSON columns for flexible algorithm configurations
- Backup and retention policies already specified

**Alternatives considered**:
- NoSQL (MongoDB) (rejected: overkill for structured data)
- File storage (rejected: doesn't meet backup requirements)

## Frontend Architecture

**Decision**: Next.js with React components and Tailwind CSS

**Rationale**:
- Server-side rendering for better SEO and performance
- Component-based architecture for reusability
- Tailwind CSS for rapid mobile-first development
- Chart.js for data visualization

**Alternatives considered**:
- Pure React SPA (rejected: worse SEO)
- Vue.js (rejected: team familiarity with React)
- Vanilla JavaScript (rejected: too much boilerplate)

## API Design

**Decision**: RESTful API with FastAPI and OpenAPI documentation

**Rationale**:
- FastAPI provides automatic OpenAPI schema generation
- Type safety with Pydantic models
- Built-in validation and error handling
- Easy to test and document

**Alternatives considered**:
- GraphQL (rejected: overkill for simple CRUD operations)
- gRPC (rejected: unnecessary complexity)

## Testing Strategy

**Decision**: Multi-layer testing with pytest, Jest, and Playwright

**Rationale**:
- Unit tests for algorithms and business logic
- Integration tests for API endpoints
- E2E tests for user workflows
- Contract tests for API compatibility

**Alternatives considered**:
- Manual testing only (rejected: doesn't meet constitution requirements)
- Only unit tests (rejected: insufficient coverage)

## Performance Optimization

**Decision**: Basic performance optimization with database indexing and caching

**Rationale**:
- Database indexes on frequently queried fields
- In-memory caching for career rules and configurations
- Static asset optimization for frontend
- Meets 1000 concurrent users requirement

**Alternatives considered**:
- Redis caching (rejected: overkill for MVP)
- CDN (rejected: not needed for initial deployment)
- Microservices (rejected: unnecessary complexity)

## Security Implementation

**Decision**: Basic security with HTTPS and password requirements

**Rationale**:
- HTTPS for all communications (already specified)
- Password minimum 8 characters (already specified)
- Basic input validation and sanitization
- No complex authentication (OAuth, SSO) for MVP

**Alternatives considered**:
- OAuth2/SSO (rejected: overkill for MVP)
- Advanced security features (rejected: not in requirements)

## Mobile-First Design

**Decision**: Responsive design with mobile-first approach

**Rationale**:
- Target users are students who primarily use mobile devices
- Progressive enhancement from mobile to desktop
- Touch-friendly interface elements
- Fast loading on mobile networks

**Alternatives considered**:
- Desktop-first design (rejected: doesn't match user behavior)
- Native mobile apps (rejected: overkill for MVP)