from flask import Flask
from config import Config
from routes import main
from models import init_db

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
init_db()

# Register Blueprint
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)

