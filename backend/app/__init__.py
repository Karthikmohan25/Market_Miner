from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend communication
    CORS(app)
    
    # Register blueprints
    from app.routes.search import search_bp
    from app.routes.trends import trends_bp
    from app.routes.analysis import analysis_bp
    from app.routes.health import health_bp
    from app.routes.chat import chat_bp
    
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(trends_bp, url_prefix='/api/trends')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    return app