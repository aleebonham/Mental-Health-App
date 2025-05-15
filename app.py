from flask import Flask
from models.models import db
from routes.routes import bp
import logging
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/app.log', level=logging.ERROR)
db.init_app(app)
app.register_blueprint(bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)