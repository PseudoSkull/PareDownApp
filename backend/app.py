import os

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from env_variables import PAREDOWN_APP_USERNAME, PAREDOWN_APP_PASSWORD, WEB_HOST_OF_PAREDOWN_APP, PAREDOWN_APP_FRONTEND_PORT

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt


ALLOWED_CORS_ORIGINS = [
    f"http://{WEB_HOST_OF_PAREDOWN_APP}:{PAREDOWN_APP_FRONTEND_PORT}",
]

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')
cors = CORS(app, resources={r"/*": 
        {
            "origins": ALLOWED_CORS_ORIGINS
        }
    },
    supports_credentials=True,
    allow_headers=['Authorization', 'Content-Type', 'Set-Cookie']
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production (HTTPS)
app.config['SESSION_COOKIE_HTTPONLY'] = True
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Flask-Login setup
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class TestDataItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(99), nullable=True, default=None)

    def __repr__(self):
        return f'<TestDataItem {self.name}>'

    def __init__(self, name, description):
        self.name = name
        self.description = description

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"message": "Logged in successfully!"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    return jsonify({"message": "Login page"}), 200

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200

@app.before_request
def restrict_access():
    if request.endpoint in ['broadcast'] and not current_user.is_authenticated:
        print("Authentication required!")
        return jsonify({"error": "Authentication required!"}), 403
    app.logger.debug('Request Headers: %s', request.headers)
    app.logger.debug('Request Body: %s', request.get_data())

@app.route('/actionendpoint', methods=['POST'])
def do_action():
    data = request.json
    action = data["action"]

    if action == "AddTestItem":
        test_item_name = data.get('name')
        test_item_description = data.get('description')

        test_item = TestDataItem(
            name = test_item_name,
            description = test_item_description
        )

        db.session.add(test_item)
        db.session.commit()

        return jsonify({"message": "Data item successfully pushed!"})

def create_admin_user():
    # db.create_all()
    if not User.query.filter_by(username=os.environ.get('PAREDOWN_APP_USERNAME', PAREDOWN_APP_USERNAME)).first():
        hashed_password = bcrypt.generate_password_hash(os.environ.get('PAREDOWN_APP_PASSWORD', PAREDOWN_APP_PASSWORD)).decode('utf-8')
        admin = User(username=os.environ.get('PAREDOWN_APP_USERNAME', PAREDOWN_APP_USERNAME), password=hashed_password)
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database and tables
        create_admin_user()
    
    app.run(debug=True)