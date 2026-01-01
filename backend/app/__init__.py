# app/__init__.py
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from celery import Celery
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Extensions
socketio = SocketIO(cors_allowed_origins="*")
celery = Celery(__name__)

def make_celery(app):
    """
    Factory to configure Celery.
    We explicitly map uppercase Flask config to lowercase Celery config
    to avoid 'ImproperlyConfigured' errors.
    """
    celery = Celery(app.import_name)
    
    # 1. Get values from Flask Config or Env
    redis_url = app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    
    # 2. Update Celery Config using ONLY lowercase keys (New Style)
    celery.conf.update(
        broker_url=redis_url,
        result_backend=redis_url,
        worker_redirect_stdouts=False,  # Fixes the Prisma/Subprocess crash
        broker_connection_retry_on_startup=True
    )

    # 3. Bind Flask Context to Tasks
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__)
    
    # --- CONFIGURATION ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret')
    
    # Redis Configuration
    # We keep these in app.config for reference, but we won't pass the whole object to Celery
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    app.config['CELERY_BROKER_URL'] = redis_url
    app.config['CELERY_RESULT_BACKEND'] = redis_url

    # Initialize Plugins
    CORS(app)
    socketio.init_app(app)
    
    # Initialize Celery
    global celery
    celery = make_celery(app)
    app.extensions["celery"] = celery

    # --- REGISTER BLUEPRINTS ---
    from .routes.auth import auth_bp
    from .routes.deploy import deploy_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(deploy_bp, url_prefix='/api/deploy')

    @app.route('/')
    def health_check():
        return {"status": "ShipIt Backend is Online 🚀", "worker": "Active"}

    return app