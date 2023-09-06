from flask import Flask
from services.crud_service import crud_service
from infrastructure.user_database import db
from controlers.user_controler import uc

app = Flask(__name__)
app.config.from_object('config')
# registering our controler named uc 
app.register_blueprint(uc, url_prefix='/')

db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
 