# Import required libraries for Flask web application
from flask_autoindex import AutoIndex  # For automatic directory browsing
import sqlite3  # For database operations
from flask import Flask, redirect, request, url_for, flash, render_template, abort, session
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from markupsafe import escape  # For safe HTML escaping
from werkzeug.security import check_password_hash, generate_password_hash  # For password security

# Create single Flask app instance
app1 = Flask(__name__)

# Set the secret key - required for sessions and flask-login
# This should be changed to a more secure key in production
app1.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Configure AutoIndex without auto-adding routes (we'll add protected routes manually)
# This allows browsing files in the /opt/reports/ directory
auto_index = AutoIndex(app1, browse_root='/opt/reports/', add_url_rules=False)

# Initialize LoginManager for handling user authentication
login_manager = LoginManager()
login_manager.init_app(app1)
login_manager.login_view = 'login'  # Redirect to login page when authentication required

# Get users from user_db.sqlite
def load_users_from_db():
    """Load active users from the SQLite database.
    
    Returns:
        dict: A dictionary mapping usernames to their hashed passwords
    """
    db_path = '/opt/user_db.sqlite'
    users = {}
    try:
        # Connect to SQLite database and fetch active users
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT username, password FROM users WHERE active = 1')
        rows = cursor.fetchall()
        
        # Build dictionary of username -> hashed_password
        for row in rows:
            users[row[0]] = row[1]  # username: hashed_password
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"Database file not found: {db_path}")
    return users


# Simple User class for demonstration
class User(UserMixin):
    """User class that inherits from Flask-Login's UserMixin.
    
    This provides default implementations for the methods that Flask-Login
    expects user objects to have (is_authenticated, is_active, is_anonymous, get_id).
    """
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        """Retrieve a user by their ID.
        
        Args:
            user_id (str): The username/ID to look up
            
        Returns:
            User: User object if found, None otherwise
        """
        users = load_users_from_db()
        if user_id in users:
            return User(user_id)
        return None

# Simple LoginForm class for demonstration
class LoginForm:
    """Simple form handler for login data.
    
    This mimics the behavior of Flask-WTF forms but without the dependency.
    """
    def __init__(self):
        # Extract username and password from the request form data
        self.username = request.form.get('username', '')
        self.password = request.form.get('password', '')
    
    def validate_on_submit(self):
        """Check if this is a POST request with required fields.
        
        Returns:
            bool: True if form is valid and submitted, False otherwise
        """
        return request.method == 'POST' and self.username and self.password

@login_manager.user_loader
def load_user(user_id):
    """Callback function for Flask-Login to reload user object from user ID stored in session.
    
    Args:
        user_id (str): The user ID stored in the session
        
    Returns:
        User: User object if found, None otherwise
    """
    return User.get(user_id)

def is_safe_url(target):
    """Check if a URL is safe for redirecting.
    
    This is a basic implementation - in production, use a more robust check.
    See http://flask.pocoo.org/snippets/62/ for a complete example.
    
    Args:
        target (str): The URL to check
        
    Returns:
        bool: True if URL is safe, False otherwise
    """
    return target and target.startswith('/')

@app1.route('/login_check')
def index():
    """Main index page that shows login status and provides navigation links.
    
    Returns:
        str: HTML response with login status and appropriate links
    """
    if current_user.is_authenticated:
        return f'Logged in as {escape(current_user.id)} please visit <a href="/files/">reports folder</a>'
    return 'You are not logged in, please visit <a href="/files/">login</a> page. If you do not have an account, please contact the administrator matthew.fisher@takealot.com to create one.'

@app1.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login - both GET (show form) and POST (process login).
    
    Returns:
        str: HTML login form for GET requests, or redirect/error for POST requests
    """
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Load users from the SQLite database
            users = load_users_from_db()
            
            # Check if user exists and password is correct using secure hash comparison
            if form.username in users and check_password_hash(users[form.username], form.password):
                user = User(form.username)
                login_user(user)  # Log the user in using Flask-Login
                flash('Logged in successfully.')
                
                # Handle redirect to originally requested page or default to index
                next_page = request.args.get('next')
                if not is_safe_url(next_page):
                    return abort(400)  # Bad request if unsafe URL
                return redirect(next_page or url_for('index'))
            else:
                flash('Invalid username or password.')
    
    # Return login form for GET requests or failed POST
    # This is a complete HTML page with modern styling
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Welcome Back</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .login-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            padding: 40px;
            width: 100%;
            max-width: 400px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .login-header {
            margin-bottom: 30px;
        }

        .login-header h1 {
            color: #333;
            font-size: 2.2rem;
            font-weight: 300;
            margin-bottom: 10px;
        }

        .login-header p {
            color: #666;
            font-size: 0.95rem;
        }

        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
            font-size: 0.9rem;
        }

        .form-input {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background-color: #fff;
            outline: none;
        }

        .form-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }

        .form-input::placeholder {
            color: #aaa;
        }

        .login-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
        }

        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 7px 20px rgba(102, 126, 234, 0.4);
        }

        .login-btn:active {
            transform: translateY(0);
        }

        .forgot-password {
            margin-top: 20px;
        }

        .forgot-password a {
            color: #667eea;
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.3s ease;
        }

        .forgot-password a:hover {
            color: #764ba2;
            text-decoration: underline;
        }

        .divider {
            margin: 30px 0;
            position: relative;
        }

        .divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #e1e5e9;
        }

        .divider span {
            background: rgba(255, 255, 255, 0.95);
            padding: 0 20px;
            color: #999;
            font-size: 0.85rem;
        }

        .social-login {
            display: flex;
            gap: 10px;
            justify-content: center;
        }

        .social-btn {
            flex: 1;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            background: white;
            color: #666;
            text-decoration: none;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }

        .social-btn:hover {
            border-color: #667eea;
            color: #667eea;
            transform: translateY(-1px);
        }

        @media (max-width: 480px) {
            .login-container {
                padding: 30px 20px;
            }
            
            .login-header h1 {
                font-size: 1.8rem;
            }
        }

        /* Animation for form appearance */
        .login-container {
            animation: slideUp 0.6s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>Welcome Back</h1>
            <p>Please sign in to your account</p>
        </div>
        
        <form method="post">
            <div class="form-group">
                <label for="username">Email</label>
                <input 
                    type="text" 
                    id="username" 
                    name="username" 
                    class="form-input" 
                    placeholder="Enter your Email"
                    required
                >
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input 
                    type="password" 
                    id="password" 
                    name="password" 
                    class="form-input" 
                    placeholder="Enter your password"
                    required
                >
            </div>
            
            <button type="submit" class="login-btn">Sign In</button>
        </form>
        
        <div class="forgot-password">
            Forgot or do not have a password? Contact <b>tdt-analytics@takealot.com</b> to reset it.
        </div>


    </div>
</body>
</html>
    '''

        # <div class="forgot-password">
        #     For new accounts, please be sure to include the following information in your email:
        #     <ul>
        #         <li>Department</li>
        #         <li>Password in the form of a link from <a href = 'https://yopass.stagealot.com;> here</a> </li>              
        #         <li>Reason for access</li>
        #     </ul>
        # </div>

@app1.route('/logout')
@login_required
def logout():
    """Handle user logout - requires user to be logged in.
    
    Returns:
        Response: Redirect to index page after logging out
    """
    logout_user()  # Flask-Login function to clear the session
    return redirect(url_for('index'))

@app1.route("/settings")
@login_required
def settings():
    """Settings page - requires authentication.
    
    Returns:
        str: Simple settings page showing current user
    """
    return f"Settings page for {escape(current_user.id)}"

# Protected file browser routes using AutoIndex
@app1.route('/')
@app1.route('/<path:path>')
@login_required
def autoindex(path='.'):
    """Protected file browser using AutoIndex.
    
    This route handles both the root path and any subpaths,
    providing a file browser interface for authenticated users.
    
    Args:
        path (str): The path within the browse_root to display
        
    Returns:
        Response: AutoIndex rendered file browser page
    """
    return auto_index.render_autoindex(path)

if __name__ == '__main__':
    # Run the Flask application
    # host='0.0.0.0' allows external connections
    # port=8000 sets the port
    # debug=True enables debug mode (should be False in production)
    app1.run(host='0.0.0.0', port=8000, debug=True)