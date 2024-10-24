from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from env_variables import PAREDOWN_APP_USERNAME, PAREDOWN_APP_PASSWORD, WEB_HOST_OF_PAREDOWN_APP, PAREDOWN_APP_FRONTEND_PORT



ALLOWED_CORS_ORIGINS = [
    f"http://{WEB_HOST_OF_PAREDOWN_APP}:{PAREDOWN_APP_FRONTEND_PORT}",
]

app = Flask(__name__)
cors = CORS(app, resources={r"/*": 
    {"origins": ALLOWED_CORS_ORIGINS}},
            supports_credentials=True) # NEEDS TO BE REMOVED FOR SECURITY REASONS IN DEPLOYMENT (probably)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class TestDataItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(99), nullable=True, default=None)

    def __repr__(self):
        return f'<TestDataItem {self.name}>'

    def __init__(self, name, description):
        self.name = name
        self.description = description

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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database and tables
    app.run(debug=True)