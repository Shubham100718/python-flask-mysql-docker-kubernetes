import os
from app import app
from flaskext.mysql import MySQL
from dotenv import load_dotenv
load_dotenv()


mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DB')
mysql.init_app(app)

