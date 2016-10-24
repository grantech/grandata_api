from flask import Flask
from flask import render_template
import sys; sys.path.insert(0, ".")
from src.common.database import Database

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "gran2016"

@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    return render_template("home.jinja2")

from src.models.users.views import user_blueprint
from src.models.stores.views import store_blueprint
from src.models.alert.views import alert_blueprint

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")

if __name__ == "__main__":
	app.run(host="0.0.0.0")
