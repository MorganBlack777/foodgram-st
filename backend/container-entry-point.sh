#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Run database migrations
echo "Running database migrations..."
python3 manage.py migrate

# Clean and collect static files
echo "Collecting static files..."
if [ -d static_backend ]; then
  rm -rf static_backend
fi

python3 manage.py collectstatic --noinput

# Copy static files to the volume
echo "Copying static files to volume..."
cp -r static_backend /static
rm -rf static_backend

# Create media directory if it doesn't exist
if [ ! -d /static/media ]; then
  echo "Creating media directory..."
  mkdir -p /static/media
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
echo "Debug mode: ${DEBUG:-0}"

if [ -z "$DEBUG" ] || [ "$DEBUG" -eq 1 ]; then
  echo "Running in development mode..."
  python3 manage.py runserver "0:8000"
else
  echo "Running in production mode..."
  gunicorn --bind 0.0.0.0:8000 backend.wsgi
fi
