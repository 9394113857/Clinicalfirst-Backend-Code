import os
from flask import Flask, jsonify
from flask_cors import CORS
from database_config import db
from flask_migrate import Migrate
from user_controller.user_routes import user
from datetime import datetime
import pytz

app = Flask(__name__)

# Ensure instance folder exists before initializing DB
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

CORS(app)

app.config['SECRET_KEY'] = 'raghu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user, url_prefix="/user")

def get_ist_time():
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    return now_ist.strftime('%Y-%m-%d %H:%M:%S')

@app.route("/")
def home():
    return jsonify({
        "message": "SQLite Flask App — Root Working",
        "current_ist_time": get_ist_time()
    })

if __name__ == "__main__":
    app.run(debug=True)
