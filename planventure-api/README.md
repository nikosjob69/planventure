# PlanVenture API

PlanVenture API is a Flask-based REST backend for managing travel plans and itineraries. It provides user authentication, protected trip routes, and a simple health endpoint for local development and frontend integration.

## Features

- User registration and login
- JWT-based authentication
- Protected trip CRUD endpoints
- Itinerary generation helper
- CORS support for React-style frontend apps
- SQLite database by default

## Tech Stack

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Python-dotenv

## Project Structure

- app.py: Flask app factory and route registration
- auth_utils.py: JWT and authentication helpers
- config.py: application configuration and environment variables
- init_db.py: initializes the SQLite database
- models: SQLAlchemy models for users and trips
- trip_routes.py: trip endpoints and itinerary generator

## Requirements

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a .env file in the project root with values such as:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///planventure.db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173
```

If you do not provide values, the app will fall back to sensible defaults.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```

   On Windows PowerShell, use:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:

   ```bash
   python init_db.py
   ```

4. Start the development server:

   ```bash
   flask run
   ```

   Or run directly:

   ```bash
   python app.py
   ```

The API will be available at:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Health Check

- GET /health

Example:

```bash
curl http://127.0.0.1:5000/health
```

### Authentication

- POST /auth/register
- POST /auth/login
- GET /auth/me

Example registration request:

```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"test1234"}'
```

### Trips

- POST /trips
- GET /trips
- GET /trips/<trip_id>
- PUT /trips/<trip_id>
- DELETE /trips/<trip_id>
- POST /trips/generate-itinerary

All trip routes require a valid JWT access token in the Authorization header:

```bash
curl -H "Authorization: Bearer <token>" http://127.0.0.1:5000/trips
```

## Example Response

Health check:

```json
{
  "status": "healthy"
}
```

## Development Notes

- Flask auto-reload is enabled when running with debug mode.
- The app uses SQLite by default, which is ideal for local development.
- CORS is configured for common React frontend development origins.

## Troubleshooting

- If the server cannot start, confirm that all dependencies are installed.
- If authentication fails, ensure the JWT token is included correctly.
- If the frontend cannot reach the API, verify that the frontend origin is listed in CORS_ORIGINS.

## License

This project is provided as part of the PlanVenture learning project.
