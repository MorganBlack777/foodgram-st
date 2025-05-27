#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Load environment variables if .env file exists
if [ -f .env ]; then
  echo "Loading environment variables from .env file..."
  set -a
  source .env
  set +a
fi

# Activate virtual environment if it exists
if [ -d venv ]; then
  echo "Activating virtual environment..."
  source venv/bin/activate
  python3 --version
fi

# Run database migrations
echo "Running database migrations..."
python3 manage.py migrate

# Collect static files if needed
if [ ! -d static_backend ]; then
  echo "Collecting static files..."
  python3 manage.py collectstatic --noinput
  mkdir -p static_backend/media
fi

# Load ingredients data
echo "Loading ingredients data..."
python3 load_ingredients.py && echo "✅ Ingredients loaded successfully" || echo "❌ Error loading ingredients"

# Load demo data if requested
if [[ "${DEMO_DATA}" == "1" ]]; then
  echo "Loading demo data..."
  if [ -f create_demo_data.py ]; then
    python3 create_demo_data.py && echo "✅ Demo data loaded successfully" || echo "❌ Error loading demo data"
  else
    echo "⚠️ Demo data script not found"
  fi
fi

# Start the server
echo "Starting server..."
echo "Debug mode: ${DEBUG:-1}"

if [ -z "$DEBUG" ] || [ "$DEBUG" -eq 1 ]; then
  echo "Running in development mode..."
  python3 manage.py runserver "0:8000"
else
  echo "Running in production mode..."
  python3 -m gunicorn --bind 0.0.0.0:8000 backend.wsgi
fi
