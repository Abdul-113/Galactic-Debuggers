from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import json
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# MongoDB Configuration
MONGO_URI = 'mongodb://localhost:27017/'
DATABASE_NAME = 'style_refresh_db'
COLLECTION_NAME = 'users'

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    users_collection = db[COLLECTION_NAME]
    print(f"✅ Connected to MongoDB: {DATABASE_NAME}.{COLLECTION_NAME}")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    users_collection = None

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Helper functions for password hashing
def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Initialize default users if collection is empty
def initialize_default_users():
    """Create default users if the collection is empty"""
    if users_collection is not None and users_collection.count_documents({}) == 0:
        default_users = [
            {
                'name': 'Admin User',
                'email': 'admin@example.com',
                'password': hash_password('admin123'),
                'role': 'teacher',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Student User',
                'email': 'student@example.com',
                'password': hash_password('student123'),
                'role': 'student',
                'created_at': datetime.utcnow()
            }
        ]
        users_collection.insert_many(default_users)
        print("✅ Default users created")

# Initialize default users
initialize_default_users()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html')

@app.route('/signup')
def signup():
    """Signup page"""
    return render_template('signup.html')

@app.route('/courses')
def courses_page():
    """Courses page"""
    return render_template('courses.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for login"""
    if users_collection is None:
        return jsonify({
            'success': False,
            'message': 'Database connection error'
        }), 500
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({
            'success': False,
            'message': 'Email and password are required'
        }), 400
    
    try:
        # Find user by email
        user = users_collection.find_one({'email': email})
        
        if user and verify_password(password, user['password']):
            # Remove password from session data
            user_session = {
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'user_id': str(user['_id'])
            }
            session['user'] = user_session
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user_session
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({
            'success': False,
            'message': 'Login failed'
        }), 500

@app.route('/api/signup', methods=['POST'])
def api_signup():
    """API endpoint for signup"""
    if users_collection is None:
        return jsonify({
            'success': False,
            'message': 'Database connection error'
        }), 500
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    
    if not all([email, password, first_name, last_name]):
        return jsonify({
            'success': False,
            'message': 'All fields are required'
        }), 400
    
    try:
        # Check if user already exists
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'User already exists'
            }), 400
        
        # Create new user
        new_user = {
            'name': f"{first_name} {last_name}",
            'email': email,
            'password': hash_password(password),
            'role': 'student',
            'created_at': datetime.utcnow()
        }
        
        result = users_collection.insert_one(new_user)
        
        # Create session data (without password)
        user_session = {
            'name': new_user['name'],
            'email': email,
            'role': 'student',
            'user_id': str(result.inserted_id)
        }
        session['user'] = user_session
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user': user_session
        })
        
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({
            'success': False,
            'message': 'Account creation failed'
        }), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """API endpoint for logout"""
    session.pop('user', None)
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

@app.route('/api/user')
def api_user():
    """Get current user info"""
    if 'user' in session:
        return jsonify({
            'success': True,
            'user': session['user']
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Not logged in'
        }), 401


@app.route('/api/upload', methods=['POST'])
def api_upload():
    """Handle course material upload"""
    if 'user' not in session:
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        }), 401
    
    if session['user']['role'] != 'teacher':
        return jsonify({
            'success': False,
            'message': 'Teacher access required'
        }), 403
    
    subject_name = request.form.get('subjectName')
    file = request.files.get('pdfUpload')
    
    if not subject_name or not file:
        return jsonify({
            'success': False,
            'message': 'Subject name and file are required'
        }), 400
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': 'No file selected'
        }), 400
    
    if file and file.filename.lower().endswith('.pdf'):
        filename = f"{subject_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'message': f'Course material uploaded successfully! Subject: {subject_name}, File: {filename}'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Only PDF files are allowed'
        }), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
