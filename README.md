# Attendance Anamoly Detection - Flask Web Application

A modern educational platform built with Flask backend and responsive frontend.

## Features

- **User Authentication**: Login and signup with session management
- **Course Management**: View available courses and enroll
- **Teacher Upload**: Teachers can upload course materials (PDF files)
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark/Light Theme**: Toggle between themes with persistent preferences
- **Modern UI**: Clean, professional interface with animations

## Project Structure

```
StyleRefresh/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── courses.html
├── static/               # Static assets
│   ├── style.css
│   ├── auth.css
│   ├── courses.css
│   ├── script.js
│   └── auth.js
└── uploads/             # Uploaded files (created automatically)
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**

   ```bash
   cd "D:\Galactic Debuggers\StyleRefresh"
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to: `http://localhost:5000`

## Usage

### Default Users

The application comes with pre-configured users for testing:

**Teacher Account:**

- Email: `admin@example.com`
- Password: `admin123`

**Student Account:**

- Email: `student@example.com`
- Password: `student123`

### Features Overview

1. **Home Page** (`/`): Landing page with hero section
2. **Login** (`/login`): User authentication
3. **Signup** (`/signup`): New user registration
4. **Courses** (`/courses`): Browse and enroll in courses
   - Teachers can upload PDF course materials
   - Students can enroll in available courses

### API Endpoints

- `POST /api/login` - User login
- `POST /api/signup` - User registration
- `POST /api/logout` - User logout
- `GET /api/user` - Get current user info
- `GET /api/courses` - Get all courses
- `POST /api/upload` - Upload course material (teachers only)
- `POST /api/enroll` - Enroll in course

## Development

### Running in Development Mode

The application runs in debug mode by default, which provides:

- Automatic reloading on code changes
- Detailed error messages
- Debug toolbar

### Customization

- **Styling**: Modify CSS files in the `static/` directory
- **Backend Logic**: Update `app.py` for server-side functionality
- **Templates**: Edit HTML files in the `templates/` directory

### Adding New Features

1. **New Routes**: Add to `app.py`
2. **New Templates**: Create in `templates/` directory

# Galactic-Debuggers — Flask Attendance & Course Demo

This repository is a small Flask web application that demonstrates a simple educational platform with user authentication, course pages, and an attendance-processing flow that can accept an uploaded attendance-sheet image and extract structured attendance data.

The app ships with a lightweight frontend (templates + static assets) and a basic in-memory user store for quick testing. It's intended as a prototype and learning reference — not production-ready.

Prototype (hosted): https://personal-1-gmmn.onrender.com

Test credentials

- Admin / Teacher
  - Email: admin@example.com
  - Password: admin123

Quick project layout

```
Galactic-Debuggers/
├── app.py              # Flask application entrypoint and routes
├── processing.py      # Attendance processing (Gemini/OpenCV variants)
├── requirements.txt   # Python dependencies
├── templates/         # Jinja2 HTML templates
└── static/            # CSS / JS / images
```

Requirements

- Python 3.8+ (Python 3.13 used during development)
- pip

Getting started (PowerShell)

1. Open PowerShell and change into the project folder:

```powershell
cd "C:\Users\ZAHID\Desktop\NEw1\Galactic-Debuggers"
```

2. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
C:\Users\ZAHID\Desktop\NEw1\Galactic-Debuggers\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Run the app:

```powershell
python .\app.py
```

5. Open the app in your browser:

http://localhost:5000

Features

- Login and signup pages with session-based auth (in-memory user store)
- Courses page and static assets
- Uploads: teachers can upload PDF course materials
- Attendance processing: UI for uploading an attendance-sheet image and extracting dates and per-student present/absent status (requires configuration if using Gemini API)

Attendance processing notes

- The repo contains two possible processing flows:

  - `processing.py` — a Gemini-based extractor (requires a valid `GOOGLE_API_KEY` in a `.env` file) that sends the uploaded image to Google Gemini to get a structured JSON response.
  - An OpenCV/Tesseract pipeline variant (also often named `processing.py` in other branches) which performs local OCR and heuristics.

- If you plan to use the Gemini-based processor, create a `.env` file next to `processing.py` with the key:

```
GOOGLE_API_KEY=your_api_key_here
```

If the key is not set, the app will return a clear runtime error from the attendance API explaining the missing key.

API endpoints (selected)

- POST /api/login – JSON { email, password }
- POST /api/signup – JSON { firstName, lastName, email, password }
- POST /api/upload – Teacher-only file upload (PDF)
- POST /api/process_attendance – Accepts multipart form image upload (attendance sheet) and returns a JSON report

Development tips

- The app runs in Flask's debug mode by default in `app.py` for rapid development. Turn off debug and set a secure `secret_key` for production.
- Replace the simple in-memory `users` dict with a real database for anything beyond demos.

Troubleshooting

- If Flask fails to start because port 5000 is in use, change the port in `app.py` or stop the conflicting process.
- If you get errors from the Gemini call, verify your `.env` and `GOOGLE_API_KEY`, and ensure your billing/API access is properly set up with your Google Cloud project.

License & Notes

This code is provided for educational/demo purposes. Do not use the development server or in-memory user store in production.

If you want, I can:

- Wire the Gemini-based `processing.py` safely so the app starts even without a key and returns friendly errors.
- Add the `/attendance` page and API endpoint (upload UI) and a small smoke-test script.
