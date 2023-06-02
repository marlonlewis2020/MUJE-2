from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './app/static/uploads') 
    RESOURCE_FOLDER = os.environ.get('RESOURCE_FOLDER', './app/static/resources') 
    
    DB_URI_STRING="mysql://{un}:{pw}@{host}/{db}"
    
    # Database credentials
    USERNAME="root"
    PASSWORD="iUZn3J31zO/w{{9n_9/NEQW!n"
    DATABASE="muje"
    HOST="localhost:3306" # other_host_options, i.e "localhost:3306", "127.0.0.1:3306", "192.168.100.90"
    
    SQLALCHEMY_DATABASE_URI = DB_URI_STRING.format(un=USERNAME,pw=PASSWORD,host=HOST,db=DATABASE) or 'sqlite:///' + os.path.join(BASEDIR, 'FESCO-TEST.db')
    