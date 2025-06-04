# Set FLASK_APP environment variable
$env:FLASK_APP = "main_app.py"

# Initialize the database
flask db init

# Create initial migration
flask db migrate -m "initial"

# Apply the migration
flask db upgrade

# Run the Flask app
python main_app.py
