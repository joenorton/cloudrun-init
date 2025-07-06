"""
Main Flask application factory for cloudrun-init.
"""
import os
from flask import Flask, g, request, jsonify
from flask_cors import CORS
from google.cloud import ndb

# Import blueprints
from app.routes import auth_bp
from app.routes.profile import profile_bp

def create_app(test_config=None):
    """Application factory pattern for Flask app."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure the app
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
            FIREBASE_PROJECT_ID=os.environ.get('FIREBASE_PROJECT_ID'),
            GOOGLE_CLOUD_PROJECT=os.environ.get('GOOGLE_CLOUD_PROJECT'),
        )
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize CORS
    CORS(app, origins=['http://localhost:3000', 'http://localhost:5000'])

    # Initialize NDB client
    try:
        from app.ndb_client import init_ndb_client
        ndb_client = init_ndb_client()
        ndb_client.context().activate()
        app.logger.info("NDB client initialized successfully")
    except Exception as e:
        # Log the error but don't fail the app startup
        app.logger.warning(f"NDB initialization failed (this is OK for local development): {e}")
        app.logger.info("NDB will not be available. Set DATASTORE_PROJECT_ID and DATASTORE_EMULATOR_HOST for local development.")
        # Set a flag to indicate NDB is not available
        app.config['NDB_AVAILABLE'] = False
    else:
        app.config['NDB_AVAILABLE'] = True

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'project': app.config.get('GOOGLE_CLOUD_PROJECT', 'local')
        })

    # Version endpoint
    @app.route('/version')
    def version():
        return jsonify({
            'version': '0.2.0',
            'phase': '0.2'
        })

    # Root endpoint
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    # Optional: Serve Firebase test files
    @app.route('/test/firebase')
    def firebase_test():
        return app.send_static_file('../test_firebase_config.html')
    
    @app.route('/test/simple')
    def simple_test():
        return app.send_static_file('../simple_firebase_test.html')

    return app


# For gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 