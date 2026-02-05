# Satellite Ship Detection

A Django web application for detecting ships in satellite images using YOLO.

## Setup Instructions

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Start the development server:
```bash
python manage.py runserver
```

4. Access the application at http://localhost:8000/

## Features

- User Registration and Login
- Ship Detection in Satellite Images
- Image Upload and Processing
- Results Visualization

## Project Structure

- `/Users` - Main application directory
- `/Templates` - HTML templates
- `/static` - Static files (CSS, JS, images)
- `/media` - Uploaded files
- `manage.py` - Django management script
