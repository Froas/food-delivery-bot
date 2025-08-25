# Food Delivery Bot

A fullstack food delivery simulation platform featuring autonomous bots, real-time order management, and interactive map visualization. The project consists of a Python FastAPI backend and a modern React (TypeScript, Vite, Tailwind) frontend. Docker and docker-compose are used for easy development and deployment.

## Features

- **Autonomous Bot Simulation:** Backend logic for managing delivery bots, routing, and movement.
- **Order Management:** Create, track, and manage food delivery orders.
- **Interactive Map:** Visualize bots, orders, and routes in real time on a grid map.
- **System Stats:** Monitor system performance and bot status.
- **REST API & WebSocket:** Real-time updates and robust API endpoints.
- **Modern Frontend:** Responsive UI built with React, TypeScript, Vite, and Tailwind CSS.
- **Containerized:** Easy setup with Docker and docker-compose.

## Project Structure

```
.
├── backend/         # FastAPI backend (Python)
│   ├── api/         # API endpoints (REST & WebSocket)
│   ├── core/        # Core configuration and database
│   ├── models/      # SQLAlchemy models
│   ├── schemas/     # Pydantic schemas
│   ├── services/    # Business logic (routing, bots, movement)
│   ├── main.py      # FastAPI app entrypoint
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/        # React frontend (TypeScript, Vite, Tailwind)
│   ├── src/         # Source code (components, hooks, services, types)
│   ├── public/      # Static assets
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env
├── BlockedPaths.csv
├── sample_data.csv
└── README.md        
```

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) & [docker-compose](https://docs.docker.com/compose/)
- (For local dev) Python 3.10+, Node.js, Bun (for frontend)

### Quick Start (Docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Froas/food-delivery-bot.git
   cd food-delivery-bot
   ```

2. **Copy and configure environment variables:**
   - Copy `.env.example` to `.env` and adjust as needed.

3. **Start all services:**
   ```bash
   docker-compose up --build
   ```
   - The backend will be available at `http://localhost:8000`
   - The frontend will be available at `http://localhost:5173`

### Local Development

#### Backend

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env` and configure as needed.

3. **Run the backend:**
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend

1. **Install dependencies:**
   ```bash
   cd frontend
   bun install
   ```

2. **Run the frontend:**
   ```bash
   bun run dev
   ```
   - The app will be available at `http://localhost:5173`

## API

- The backend exposes RESTful endpoints under `/api/v1/` (orders, bots, routes, map, etc.)
- WebSocket endpoint for real-time updates: `/api/v1/websocket`
- See source code in `backend/api/v1/` for details.

## Environment Variables

- `.env` files are used for configuration (database URL, secret keys, etc.)
- See `.env.example` or backend/core/config.py for required variables.

## Sample Data

- `BlockedPaths.csv` and `sample_data.csv` provide initial data for the simulation.
- Use `backend/init_data.py` and `backend/init_blocked_paths.py` to initialize the database.

## Development Notes

- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, Bun
- **Testing:** (Add instructions if tests are available)
- **Linting/Formatting:** (Add instructions if applicable)

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

[MIT](LICENSE) (or specify your license here)
