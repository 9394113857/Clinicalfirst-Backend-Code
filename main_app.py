from flask import Flask
from database_config import db
from flask_migrate import Migrate
from user_controller.user_routes import user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'raghu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user, url_prefix="/user")

@app.route("/")
def home():
    return "<h2>SQLite Flask App — Root Working</h2>"

if __name__ == "__main__":
    app.run(debug=True)
