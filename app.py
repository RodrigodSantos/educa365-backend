from flask import Flask

from helpers.cors import cors
from helpers.api import api, api_bp
from helpers.config import get_config
from helpers.database import db, migrate

# Create the app
app = Flask(__name__)

# Configurations
app.config.from_object(get_config())

# Api e Blueprint
api.init_app(app)

# Cors
cors.init_app(app)

# Database
db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(api_bp)

if __name__ == '__main__':
  app.run(debug=True)