#!/bin/bash

# Navigate to your Flask project directory
cd C:\Users\cemc\Documents\YTPopupPlayer\backend\app.py

# Redirect standard error to standard output
exec 2>&1

echo "Initializing Flask migration..."
flask db init
echo "Flask migration initialized."

echo "Creating a migration script..."
flask db migrate
echo "Migration script created."

echo "Applying the database migrations..."
flask db upgrade
echo "Database migrations applied."
