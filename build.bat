@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo  Starting Django Build ^& Deployment Script
echo ==========================================

:: Step 1: Install dependencies
echo --^> Installing dependencies from requirements.txt...
python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
echo [ERROR] Failed to upgrade pip. Exiting...
exit /b %ERRORLEVEL%
)

pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
echo [ERROR] Failed to install dependencies. Exiting...
exit /b %ERRORLEVEL%
)

:: Step 2: Collect static files
echo --^> Collecting static files...
python manage.py collectstatic --no-input
if %ERRORLEVEL% neq 0 (
echo [ERROR] Failed to collect static files. Exiting...
exit /b %ERRORLEVEL%
)

:: Step 3: Database migrations
echo --^> Preparing migrations...
python manage.py makemigrations
if %ERRORLEVEL% neq 0 (
echo [ERROR] Failed to create migrations. Exiting...
exit /b %ERRORLEVEL%
)

echo --^> Applying database migrations...
python manage.py migrate
if %ERRORLEVEL% neq 0 (
echo [ERROR] Failed to apply migrations. Exiting...
exit /b %ERRORLEVEL%
)

:: Step 4: Seed initial data (optional / custom command)
echo --^> Seeding database with initial data...
python manage.py seed_db
if %ERRORLEVEL% equ 0 (
echo     Database seeded successfully.
) else (
echo     Warning: Seeding step was skipped or already applied.
)

:: Step 5: Start the application
:: Note: In production environments, use a WSGI/ASGI server (e.g., Waitress on Windows) instead of runserver.
echo ==========================================
echo  Build completed! Starting Django server...
echo ==========================================
python manage.py runserver