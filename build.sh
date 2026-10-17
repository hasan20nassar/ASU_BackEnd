#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
# Treat unset variables as an error
# Prevent errors in a pipeline from being masked
set -euo pipefail

echo "=========================================="
echo " Starting Django Build & Deployment Script"
echo "=========================================="

# Step 1: Install dependencies
echo "--> Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 2: Collect static files
echo "--> Collecting static files..."
python manage.py collectstatic --no-input

# Step 3: Database migrations
echo "--> Applying database migrations..."
python manage.py migrate

# Step 4: Seed initial data (optional / custom command)
echo "--> Seeding database with initial data..."
if python manage.py seed_db; then
    echo "    Database seeded successfully."
else
    echo "    Warning: Seeding step was skipped or already applied."
fi

echo "=========================================="
echo " Build completed successfully!"
echo "=========================================="